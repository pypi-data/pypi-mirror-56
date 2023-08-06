import click
import requests


@click.command()
@click.option('-o', '--owner', help='Owner account name')
@click.option('-q', '--queue-id', help='Job queue ID')
@click.pass_context
def ls(ctx, owner, queue_id):
    """
    Listing workflow queues
    """
    jess_url = ctx.obj.get('JT_CONFIG').get('jess_server')
    if not owner:
        owner = ctx.obj.get('JT_CONFIG').get('jt_account')

    url = "%s/queues/owner/%s" % (jess_url, owner)
    if queue_id:
        url += '/queue/%s' % queue_id

    r = requests.get(url)

    if r.status_code != 200:
        click.echo('List job queue for: %s failed: %s' % (owner, r.text))
    else:
        click.echo(r.text)


@click.command()
@click.option('-n', '--wf-name', required=True, help='Workflow name')
@click.option('-v', '--wf-version', required=True, help='Workflow version')
@click.option('-o', '--wf-owner', help='Workflow owner account name')
@click.pass_context
def add(ctx, wf_name, wf_version, wf_owner):
    """
    Create a workflow queue
    """
    jess_url = ctx.obj.get('JT_CONFIG').get('jess_server')
    if wf_owner is None:
        wf_owner = ctx.obj.get('JT_CONFIG').get('jt_account')

    url = "%s/queues/owner/%s/workflow/%s/ver/%s" % (jess_url, wf_owner, wf_name, wf_version)

    r = requests.post(url)
    if r.status_code != 200:
        click.echo('Queue creation for: %s failed: %s' % (wf_owner, r.text))
    else:
        click.echo("Queue registration succeeded, details as below")
        click.echo(r.text)


@click.command()
@click.option('-q', '--queue-id', required=True, help='Queue ID')
def pause(queue_id):
    """
    Pause a workflow queue
    """
    r = update_queue_state(queue_id, 'pause')

    if r.status_code != 200:
        click.echo('Pause queue failed, please ensure input is correct.')
    else:
        click.echo(r.text)


@click.command()
@click.option('-q', '--queue-id', required=True, help='Queue ID')
def open(queue_id):
    """
    Open a workflow queue
    """
    r = update_queue_state(queue_id, 'open')

    if r.status_code != 200:
        click.echo('Open queue failed, please ensure input is correct.')
    else:
        click.echo(r.text)


@click.command()
@click.option('-q', '--queue-id', required=True, help='Queue ID')
def close(queue_id):
    """
    Close a workflow queue
    """
    r = update_queue_state(queue_id, 'close')

    if r.status_code != 200:
        click.echo('Close queue failed, please ensure input is correct.')
    else:
        click.echo(r.text)


@click.pass_context
def update_queue_state(ctx, queue_id, action):
    jess_url = ctx.obj.get('JT_CONFIG').get('jess_server')
    owner = ctx.obj.get('JT_CONFIG').get('jt_account')

    url = "%s/queues/owner/%s/queue/%s/action" % (jess_url, owner, queue_id)

    request_body = {
        'action': action
    }

    return requests.put(url, json=request_body)
