import os
import sys
import zipfile
import tempfile
from io import BytesIO
import requests
import shutil
import subprocess
import errno
import yaml
import click
import signal
import socket
import multiprocessing
from time import sleep
from uuid import uuid4
from .scheduler import JessScheduler
from .scheduler import LocalScheduler
from .worker import Worker


def get_node_ip():
    try:
        return [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1][0]
    except:
        try:
            return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close())
                        for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
        except:
            return '127.0.0.1'


class GracefulKiller:
    def __init__(self, logger):
        self.kill_now = False
        self.logger = logger
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.logger.info('Interruption signal received, will exit when the current running job finishes.')
        self.kill_now = True


def work(worker, logger):
    proc_name = multiprocessing.current_process().name
    try:
        rv = worker.run()
        logger.info('Finish task: {} by worker: {}'.format(proc_name, worker.id))
    except:
        # for server mode:
        # if exception happened, worker might not have reported failure to the server
        # need to check the server and report as needed
        pass


class Executor(object):
    def __init__(self, jt_home=None, jt_account=None,
                 ams_server=None, wrs_server=None, jess_server=None,
                 queue_id=None,
                 workflow_name=None,
                 job_file=None,  # when job_file is provided, it's local mode, no tracking from the server side
                 job_selector=None,  # can optionally specify which job to run, not applicable when job_file specified
                 min_disk=None, # minimally require disk space (in bytes) for launching task execution
                 parallel_jobs=1, parallel_workers=1, polling_interval=10, max_jobs=0,
                 continuous_run=True, retries=2,
                 force_restart=False, resume_job=False, logger=None):

        self._killer = GracefulKiller(logger)

        # TODO: will need to verify jt_account

        self._jt_home = jt_home
        self._account_id = None
        self._queue_id = queue_id

        self._parallel_jobs = parallel_jobs
        self._max_jobs = max_jobs
        self._min_disk = min_disk
        self._parallel_workers = parallel_workers
        self._polling_interval = polling_interval
        self._ran_jobs = 0
        self._continuous_run = continuous_run
        self._retries = retries
        self._force_restart = force_restart
        self._resume_job = resume_job

        self._running_jobs = []
        self._worker_processes = {}
        self._logger = logger
        self._node_ip = get_node_ip()

        # params for server mode
        if self.queue_id and job_file is None:
            # the logic is a bit bad here, we need to get account_id for init jthome, and get node_id
            self._scheduler = JessScheduler(jess_server=jess_server,
                                            wrs_server=wrs_server,
                                            ams_server=ams_server,
                                            jt_account=jt_account,
                                            queue_id=queue_id,
                                            )

            self._account_id = self.scheduler.account_id
            self._jt_account = jt_account

            # init jt_home dir
            self._init_jt_home()

            self._id = self.scheduler.register_executor(self.node_id, self.node_ip)  # reset executor ID to what server side return

            # update job selector if supplied
            if job_selector is not None:
                self.scheduler.update_executor(action={
                    'job_selector': job_selector
                })

        # local mode if supplied, local mode does NOT work
        elif job_file and self.queue_id is None:
            self._scheduler = LocalScheduler(job_file=job_file,
                                             workflow_name=workflow_name,
                                             executor_id=self.id)

            self._id = str(uuid4())  # self-assigned executor ID for local mode

        else:
            raise Exception('Please specify either queue_id for executing jobs on remote job queue or '
                            'job_file to run local job.')

        # init workflow dir
        self._init_workflow_dir()

        # init queue dir
        self._init_queue_dir()

        # init executor dir
        self._init_executor_dir()

        # clean up any jobs left in `running` state on the server
        self._clean_up_running_jobs()

        logger.info("Executor: %s started." % self.id)

    @property
    def killer(self):
        return self._killer

    @property
    def id(self):
        return self._id

    @property
    def node_ip(self):
        return self._node_ip

    @property
    def logger(self):
        return self._logger

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def jt_home(self):
        return self._jt_home

    @property
    def jt_account(self):
        return self._jt_account

    @property
    def account_id(self):
        return self._account_id

    @property
    def node_id(self):
        return self._node_id

    @property
    def queue_id(self):
        return self._queue_id

    @property
    def node_dir(self):
        return os.path.join(self.jt_home, 'account.%s' % self.account_id, 'node')

    @property
    def workflow_dir(self):
        return os.path.join(self.node_dir,
                            'workflow.%s' % self.scheduler.workflow_id,
                            self.scheduler.workflow_version)

    @property
    def queue_dir(self):
        return os.path.join(self.workflow_dir, 'queue.%s' % self.scheduler.queue_id)

    @property
    def executor_dir(self):
        return os.path.join(self.queue_dir, 'executor.%s' % self.scheduler.executor_id)

    @property
    def polling_interval(self):
        return self._polling_interval

    @property
    def parallel_jobs(self):
        return self._parallel_jobs

    @property
    def max_jobs(self):
        return self._max_jobs

    @property
    def min_disk(self):
        return self._min_disk

    @property
    def parallel_workers(self):
        return self._parallel_workers

    @property
    def running_jobs(self):
        return self._running_jobs

    @property
    def ran_jobs(self):
        return self._ran_jobs

    @property
    def continuous_run(self):
        return self._continuous_run

    @property
    def retries(self):
        return self._retries

    @property
    def force_restart(self):
        return self._force_restart

    @property
    def resume_job(self):
        return self._resume_job

    @property
    def worker_processes(self):
        return self._worker_processes

    def run(self):
        if self.scheduler.mode == 'local':
            self._run_local()
        else:
            self._run_remote()

    def _run_local(self):
        # TODO: local run is more complicated, let's worry about it later
        click.echo('Run local job not implemented yet.')

    def _run_remote(self):
        while True:
            if self.killer.kill_now:
                self.logger.info('Received interruption signal, will not pick up new job. Exit after finishing current '
                           'running job (if any) ...')
                break

            running_jobs, running_workers = self._get_run_status()

            # check whether workdir has enough disk space to continue
            if not self._enough_disk():
                if self.continuous_run:
                    self.logger.info('No enough disk space, will start new job when enough space is available.')
                    self.logger.info("Current running jobs: %s, running tasks: %s" % (running_jobs, running_workers))
                    sleep(self.polling_interval)  # TODO: may want to have a smarter wait intervals
                    continue
                else:
                    self.logger.info('No enough disk space, exit after finishing current running job (if any) ...')
                    self.logger.info("Current running jobs: %s, running tasks: %s" % (running_jobs, running_workers))
                    break

            if self.max_jobs and self.ran_jobs >= self.max_jobs:
                job_count_text = 'job has' if self.max_jobs == 1 else 'jobs have'
                self.logger.info('Total number of executed %s reached preset limit of %s, relevant tasks are either '
                           'finished or scheduled, executor will exit after running tasks finish ...' %
                           (job_count_text, self.max_jobs)
                           )
                break

            if running_jobs >= self.parallel_jobs:
                # basically we check again to see if running jobs drop to under the parallel limit
                # detail: we need to worry about possible run-away job, job appears to be running but worker died
                #         already, is that possible if executor is still alive? Can executor report the state of a
                #         task ran by a worker whose process exited with error?
                self.logger.info('Reached limit for parallel running jobs, will start new job after completing a current job.')
                self.logger.info("Current running jobs: %s, running tasks: %s" % (running_jobs, running_workers))

                sleep(self.polling_interval)
                continue

            worker = Worker(jt_home=self.jt_home, account_id=self.account_id, retries=self.retries,
                            scheduler=self.scheduler, node_id=self.node_id, node_ip=self.node_ip, logger=self.logger)

            # get a task from a new job, break if no task returned, which suggests there is no more job
            if not worker.next_task(job_state='queued'):
                if self.continuous_run:
                    self.logger.info('No job in the queue, will start new job as it arrives.')
                    self.logger.info("Current running jobs: %s, running tasks: %s" % self._get_run_status())
                    sleep(self.polling_interval)  # TODO: may want to have a smarter wait intervals
                    continue
                else:
                    self.logger.info('No job in the queue. Exit after finishing current running job (if any) ...')
                    self.logger.info("Current running jobs: %s, running tasks: %s" % self._get_run_status())
                    break

            # start the task
            p = multiprocessing.Process(target=work,
                                        name='task:%s job:%s' % (worker.task.get('name'), worker.task.get('job.id')),
                                        args=(worker, self.logger)
                                        )

            self._worker_processes[worker.task.get('job.id')] = [p]
            p.start()

            # this is the first task of a new job
            self._ran_jobs += 1
            self.logger.info('Executor: %s starts no. %s job' % (self.id, self.ran_jobs))

            shutdown = False
            # stay in this loop when there are tasks to be run related to current running jobs
            while self.scheduler.has_next_task():
                sleep(self.polling_interval)
                if self.killer.kill_now:
                    self.logger.info(
                        'Received interruption signal, will not pick up new task. Exit when current running task(s) '
                        'finishes...')
                    shutdown = True
                    break

                running_jobs, running_workers = self._get_run_status()

                self.logger.info('Current running jobs: %s, running tasks: %s' % (running_jobs, running_workers))

                if not running_workers < self.parallel_workers:
                    continue

                worker = Worker(jt_home=self.jt_home, account_id=self.account_id, retries=self.retries,
                                scheduler=self.scheduler, node_id=self.node_id, node_ip=self.node_ip, logger=self.logger)

                task = worker.next_task(job_state='running')  # get next task in the current running jobs

                if not task:  # if no task, try to start task for next job if it's appropriate to do so
                    if (self.max_jobs and self.ran_jobs >= self.max_jobs) or \
                            len(self.scheduler.running_jobs()) >= self.parallel_jobs:
                        # no free slot, so not to start any new job
                        continue

                    # check whether workdir has enough disk space to continue
                    if not self._enough_disk():
                        self.logger.info('No enough disk space, will start new job when enough space is available.')
                        self.logger.info("Current running jobs: %s, running tasks: %s" % self._get_run_status())
                        # on enough space, not to start any new job, will continue with remaining tasks of running jobs
                        continue

                    task = worker.next_task(job_state='queued')
                    if task:
                        self._ran_jobs += 1
                        self.logger.info('Executor: %s starts no. %s job' % (self.id, self.ran_jobs))

                if task:
                    p = multiprocessing.Process(target=work,
                                            name='task:%s job:%s' % (worker.task.get('name'), worker.task.get('job.id')),
                                            args=(worker, self.logger)
                                            )
                    if not self.worker_processes.get(worker.task.get('job.id')):
                        self._worker_processes[worker.task.get('job.id')] = [p]
                    else:
                        self._worker_processes[worker.task.get('job.id')].append(p)
                    p.start()

            if shutdown:
                break

        while not self.killer.kill_now and len(self.scheduler.running_jobs()): # no cancel, then wait until all running tasks finish
            self.logger.info("Current running jobs: %s, running tasks: %s" % self._get_run_status())
            sleep(self.polling_interval)
            continue

        for j in self.worker_processes:
            for p in self.worker_processes.get(j):
                if p.is_alive():
                    self.logger.debug('Killing subprocess: %s' % p)
                    os.kill(p.pid, signal.SIGKILL)  # there is no point to wait for worker process

        # call server to mark this executor terminated
        if self.killer.kill_now:
            for j in self.scheduler.running_jobs():
                self.logger.info('Cancelling job: %s' % j.get('id'))
                self.scheduler.cancel_job(job_id=j.get('id'))

        try:
            os.remove(os.path.join(self.executor_dir, '_state.running'))
        except OSError:
            pass

        # report summary about completed jobs and running jobs if any
        self.logger.info('Executed %s %s.' % (self.ran_jobs, 'job' if self.ran_jobs <= 1 else 'jobs'))

    def _get_run_status(self):
        running_workers = 0
        running_jobs = 0
        for j in self.scheduler.running_jobs():
            self.logger.info('Running job: %s' % j.get('id'))
            running_jobs += 1
            for p in self.worker_processes.get(j.get('id'), []):
                if p.is_alive():
                    self.logger.info('Running task: %s' % p.name)
                    running_workers += 1
                    p.join(timeout=0.1)
        return running_jobs, running_workers

    def _init_jt_home(self):
        # initial it if needed
        node_info_file = os.path.join(self.node_dir,'info.yaml')

        if os.path.isfile(node_info_file):  # if info.yaml exists, use everything in it
            with open(node_info_file, 'r') as f:
                node_info = yaml.load(f)
        else:  # not exist
            node_info = {'id': str(uuid4()), 'node_ip': self.node_ip}  # may need to add other information
            try:
                os.makedirs(self.node_dir)
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            with open(node_info_file, "w") as f:
                f.write(yaml.dump(node_info, default_flow_style=False))

        self._node_id = node_info.get('id')
        self._node_ip = node_info.get('node_ip')

    def _init_workflow_dir(self):
        try:
            os.makedirs(self.workflow_dir)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

        # detect whether workflow has already been installed
        workflow_installation_flag_file = os.path.join(self.workflow_dir, 'workflow.installed')
        if os.path.isfile(workflow_installation_flag_file):
            return

        self.logger.info('Installing workflow package ...')
        workflow = self.scheduler.get_workflow()

        git_account = workflow.get('git_account')
        git_repo = workflow.get('git_repo')
        git_tag = workflow.get('ver:%s' % self.scheduler.workflow_version).get('git_tag')
        git_path = workflow.get('ver:%s' % self.scheduler.workflow_version).get('git_path')

        # https://github.com/jthub/jtracker-example-workflows/archive/0.2.0.tar.gz
        git_download_url = "https://github.com/%s/%s/archive/%s.zip" % (git_account, git_repo, git_tag)

        tmp_dir = tempfile.mkdtemp()
        request = requests.get(git_download_url)
        zfile = zipfile.ZipFile(BytesIO(request.content))
        zfile.extractall(tmp_dir)

        source_workflow_path = os.path.join(tmp_dir, '%s-%s' % (git_repo, git_tag), git_path, 'workflow')
        source_tool_path = os.path.join(source_workflow_path, 'tools')
        if os.path.isdir(source_tool_path):
            subprocess.check_output(["chmod", "-R", "755", source_tool_path])

        # rm first in case exist
        shutil.rmtree(os.path.join(self.workflow_dir, 'workflow'), ignore_errors=True)

        shutil.move(source_workflow_path, self.workflow_dir)

        # now create the installation flag file
        open(workflow_installation_flag_file, 'a').close()
        self.logger.info('Workflow package installed')

    def _init_queue_dir(self):
        try:
            os.makedirs(self.queue_dir)
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    def _init_executor_dir(self):
        try:
            os.makedirs(self.executor_dir)
        except OSError as e:  # Guard against race condition
            if e.errno != errno.EEXIST:
                raise

        flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
        try:
            os.open(os.path.join(self.executor_dir, '_state.running'), flags)
        except OSError as e:
            if e.errno == errno.EEXIST:  # Exit as the executor is running.
                if not (self.force_restart or self.resume_job):
                    self.logger.info('The executor: %s for queue: %s is running on this node: %s already, not start executor without -f or -r option.'
                          % (self.id, self.queue_id, self.node_id))
                    sys.exit(1)
            else:
                self.logger.info('Unable to start executor, write permission is needed in JTHome')
                sys.exit(1)

    def _clean_up_running_jobs(self):
        server_running_jobs = self.scheduler.running_jobs()
        if server_running_jobs:
            if not (self.resume_job or self.force_restart):
                self.logger.info('Server reports running jobs by the executor on this compute node, not start executor without -f or -r option.')
                sys.exit(1)

            for j in server_running_jobs:
                if self.resume_job:
                    self.logger.info('Set previous running job: %s to resume' % j.get('id'))
                    self.scheduler.resume_job(j.get('id'))
                elif self.force_restart:
                    self.logger.info('Cancel previous running job: %s' % j.get('id'))
                    self.scheduler.cancel_job(j.get('id'))

    def _enough_disk(self):
        statvfs = os.statvfs(self.executor_dir)

        if self.min_disk is not None \
            and self.min_disk != 0 \
            and statvfs.f_bavail * statvfs.f_frsize < self.min_disk:
            return False

        return True
