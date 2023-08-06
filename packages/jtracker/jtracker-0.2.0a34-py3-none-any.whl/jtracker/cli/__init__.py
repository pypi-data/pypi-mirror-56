import os
import logging
import yaml
import click
import click_log
from jtracker import __version__ as ver
from .user import commands as user_commands
from .org import commands as org_commands
from .wf import commands as wf_commands
from .queue import commands as queue_commands
from .job import commands as job_commands
from .task import commands as task_commands
from .exec import commands as exec_commands
from .conf import commands as conf_commands

from .config import Config

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('JTracker cli %s' % ver)
    ctx.exit()


def setup(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    config_file = os.path.join(os.getenv("HOME"), '.jtconfig')
    jt_home = os.path.join(os.getenv("HOME"), 'jthome')

    # hardcode this for now
    conf_dict = {
                  "jt_account": "user1",
                  "ams_server": "https://jtracker.io/api/jt-ams/v0.1",
                  "wrs_server": "https://jtracker.io/api/jt-wrs/v0.1",
                  "jess_server": "https://jtracker.io/api/jt-jess/v0.1",
                  "jt_home": jt_home
                }

    with open(config_file, "w") as c:
        c.write(yaml.dump(conf_dict, default_flow_style=False))

    click.echo('==================================================')
    click.echo()
    click.echo(yaml.dump(conf_dict, default_flow_style=False))
    click.echo('==================================================')
    click.echo("You may edit configuration file '%s' for any changes." % config_file)
    click.echo()
    ctx.exit()


@click.group()
@click.option('--write-out', '-w', type=click.Choice(['simple', 'json']),
              default='simple', help='JT-CLI output format', required=False)
@click.option('--config-file', '-c', envvar='JT_CONFIG_FILE', type=click.Path(exists=True),
              help='JTracker configuration file', required=False)
@click.option('--version', '-v', is_flag=True, callback=print_version, expose_value=False,
              help='Show JTracker version', is_eager=True)
@click.option('--setup', '-s', is_flag=True, callback=setup, expose_value=False,
              help='Complete JTracker CLI configuration', is_eager=True)
@click.pass_context
@click_log.simple_verbosity_option(logger, '--verbosity', '-V')
def main(ctx, config_file, write_out):
    # initialize configuration from config_file
    if config_file is None:
        config_file = os.path.join(os.getenv("HOME"), '.jtconfig')

    try:
        jt_config = Config(config_file).dict
    except Exception as err:
        click.echo(str(err))
        click.echo("Please run 'jt --setup' to complete JTracker CLI configuration")
        ctx.exit()

    # initializing ctx.obj
    ctx.obj = {
        'JT_WRITE_OUT': write_out,
        'JT_CONFIG_FILE': config_file,
        'JT_CONFIG': jt_config,
        'LOGGER': logger
    }


@main.group()
@click.pass_context
def config(ctx):
    """
    View or update JT cli configuration
    """
    pass

config.add_command(conf_commands.show)
config.add_command(conf_commands.update)


@main.group()
@click.pass_context
def user(ctx):
    """
    Operations related to user
    """
    pass

# user subcommands
user.add_command(user_commands.ls)
user.add_command(user_commands.login)
user.add_command(user_commands.whoami)
user.add_command(user_commands.signup)
user.add_command(user_commands.delete)
user.add_command(user_commands.update)


@main.group()
@click.pass_context
def org(ctx):
    """
    Operations related to organization
    """
    pass


# org subcommands
org.add_command(org_commands.ls)


@main.group()
@click.pass_context
def wf(ctx):
    """
    Operations related to workflow
    """
    pass


# wf subcommands
wf.add_command(wf_commands.ls)
wf.add_command(wf_commands.register)


@main.group()
@click.pass_context
def queue(ctx):
    """
    Operations related to queue
    """
    pass


# queue subcommands
queue.add_command(queue_commands.ls)
queue.add_command(queue_commands.add)
queue.add_command(queue_commands.pause)
queue.add_command(queue_commands.close)
queue.add_command(queue_commands.open)


@main.group()
@click.pass_context
def job(ctx):
    """
    Operations related to job
    """
    pass


# job subcommands
job.add_command(job_commands.ls)
job.add_command(job_commands.get)
job.add_command(job_commands.delete)
job.add_command(job_commands.resume)
job.add_command(job_commands.reset)
job.add_command(job_commands.suspend)
job.add_command(job_commands.add)


@main.group()
@click.pass_context
def task(ctx):
    """
    Operations related to task
    """
    pass


# task subcommands
task.add_command(task_commands.ls)


@main.group()
@click.pass_context
def exec(ctx):
    """
    Operations related to executor
    """
    pass


# exec subcommands
exec.add_command(exec_commands.run)
exec.add_command(exec_commands.ls)
exec.add_command(exec_commands.selector)


if __name__ == '__main__':
    main()
