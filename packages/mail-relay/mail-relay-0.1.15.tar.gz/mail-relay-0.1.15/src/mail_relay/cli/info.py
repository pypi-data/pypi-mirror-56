import pprint

import click

from .context import ctx


@click.command()
@click.option('--org-info', 'show_org_info', flag_value=True, default=False)
@click.option('--export-group', 'show_export_group', flag_value=True, default=False)
@click.option('--members', 'show_members', flag_value=True, default=False)
@ctx
def info(ctx, show_org_info, show_export_group, show_members):
    '''Show information about organization, export groups and members.'''
    from mail_relay.store.handlers import read_users, read_exporter

    exporter_a_v, exporter_id = read_exporter(ctx.store.path)
    if not exporter_id:
        click.echo('No exporter configured! Try configuring exporter '
                   '```relay config exporter ${user_id}```, then try again.')
        return

    exporter = read_users(ctx.store.path)[(exporter_a_v, exporter_id)]

    org_info = ctx.cs_client.get_org_info(exporter, exporter.org_info.org_id)
    pp = pprint.PrettyPrinter(indent=4, )

    if (show_org_info or show_export_group or show_members) is False:  # show all if not specified
        click.echo(pp.pformat(org_info))
    else:
        if show_org_info:  # get org info
            # latest user versions
            o = dict(org_info)
            del o['users']
            click.echo(pp.pformat(o))

        # get export group info
        # get approvers/exporter info
        if show_export_group:
            if org_info['roled_approval_groups'].get('export_approval_group') is None:
                click.echo('No export group configured! create and '
                           'set an export group for your organization and try again.')
                return
            group_id = org_info['roled_approval_groups']['export_approval_group']['group_id']
            version = org_info['roled_approval_groups']['export_approval_group']['version']
            export_group = ctx.cs_client.get_org_apg_info(
                exporter, exporter.org_info.org_id, group_id, version)
            click.echo(pp.pformat(export_group))

        # get members info
        if show_members:
            click.echo(pp.pformat(org_info['users']))
