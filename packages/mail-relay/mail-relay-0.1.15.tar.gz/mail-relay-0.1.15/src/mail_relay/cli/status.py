import click

from .context import ctx


@click.group(invoke_without_command=True)
@click.pass_context
def status(gctx):
    '''Check status of relay daemon'''

    if gctx.invoked_subcommand is None:
        click.echo('daemon status check')


@click.command()
@click.option('-t', '--test-send', 'test_send', flag_value=True, default=False)
@ctx
def smtp(ctx, test_send):
    '''Check smtp connection status'''
    from mail_relay.mail import test_smtp_connection, send_test_mail, create_test_mime

    click.echo('checking smtp status for \r\n {}\r\n'.format(ctx.config.smtp.to_json()))
    test_smtp_connection(ctx.config.smtp)

    if test_send:
        m = create_test_mime('saman@preveil.com', ['saman@preveil.com'])
        # TODO: check result, handle failures
        result = send_test_mail(ctx.config.smtp, m)
        print result


status.add_command(smtp)
