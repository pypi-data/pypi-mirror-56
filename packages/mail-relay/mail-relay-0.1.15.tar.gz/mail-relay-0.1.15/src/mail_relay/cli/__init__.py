import click

from mail_relay.store import DEFAULT_STORE_PATH, Store
from mail_relay.store.handlers import read_config

from .config import config
from .context import Context, ctx
from .info import info
from .start import start
from .status import status
from .start import start


@click.group()
@click.option(
    '-p', '--store-path', 'store_path',
    type=click.Path(dir_okay=False),
    default=DEFAULT_STORE_PATH, show_default=True,
    help='Path to sqlite store.')
@click.option(
    '--store-version', 'store_version',
    type=click.INT,
    default=0, show_default=True,
    help='sqlite store version.')
@click.pass_context
def driver(gctx, store_path, store_version):
    '''relay is a simple cli tool that relays preveil emails to a configurable smtp server'''

    # Initiate context object
    store = Store(store_path, store_version)
    config = None
    if gctx.invoked_subcommand != 'migrate':
        config = read_config(store.path)
        if config is None:
            if gctx.invoked_subcommand != 'config':
                click.echo('No config set. configure using `-c/--config-file`!')
                gctx.exit(0)

    gctx.obj = Context(store, config)


@click.command()
@ctx
def migrate(ctx):
    '''Migrate database using mail_rely/migrate.py (or optional script).'''
    # TODO dynamic migrate script
    from mail_relay.store.migrate import migrate
    migrate(ctx.store.path)


driver.add_command(info)
driver.add_command(config)
driver.add_command(migrate)
driver.add_command(start)
driver.add_command(status)
driver.add_command(start)
