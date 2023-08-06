import click
from mail_relay.daemon.main import main

from .context import ctx


@click.command()
@click.option('--members', 'members', required=False, multiple=True)
@ctx
def start(ctx, members):
    '''Start relay daemon.'''
    from mail_relay.store.handlers import read_exporter

    exporter_a_v, exporter_id = read_exporter(ctx.store.path)
    if not exporter_id:
        click.echo('No exporter configured! Try configuring exporter '
                   '```relay config exporter ${user_id}```, then try again.')
        return

    main(ctx.store.path, members)
