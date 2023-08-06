import os

import click
from pvHelpers.crypto_client import CryptoClient
from pvHelpers.cs_client import BackendClient
from pvHelpers.utils import CaseInsensitiveDict, jdumps, randUnicode

from .utils import add_member, create_export_group, create_new_org, generate_load


@click.command('generate')
@click.option(
    '-u', '--admin-user', 'admin_user',
    required=False,
    default=None,
    type=click.STRING)
@click.option('-c', '--create-org', 'create_org', flag_value=True, default=False)
@click.pass_context
def generate(gctx, admin_user, create_org):
    '''generate mail load on an organization'''

    cs_client = BackendClient()
    cs_client.init(unicode(os.environ['CS_URL']))
    crypto_client = CryptoClient(unicode(os.environ['CRYPTO_URL']))

    if create_org:
        if len(crypto_client.list_local_users()['users']):
            click.echo('Already configured!')

            gctx.exit(1)

        admin_id = u'{}@preveil.test'.format(randUnicode())
        admin = create_new_org(admin_id, crypto_client)

        export_group_size = (int(os.environ.get('EXPORT_GROUP_SIZE', 3)), int(os.environ.get('OPTIONALS_REQUIRED', 1)))
        approvers = []
        for _ in xrange(export_group_size[0]):
            approvers.append(add_member(admin, crypto_client, cs_client))

        group = create_export_group(admin, approvers, export_group_size[1], crypto_client)
        click.echo(jdumps({
            'admin_id': admin['user_id'],
            'org_id': admin['org_info']['org_id'],
            'export_group': group,
            'optionals_required': export_group_size[1],
            'approvers': [{'user_id': a['user_id'], 'account_version': 0} for a in approvers]
        }))

        gctx.exit(0)

    if admin_user is None:
        click.echo('Should provide admin user_id via `-u/--admin-user`!')
        gctx.exit(1)

    generate_load(admin_user, cs_client, crypto_client)


generate()
