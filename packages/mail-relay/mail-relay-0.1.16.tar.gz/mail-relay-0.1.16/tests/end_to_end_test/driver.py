import time

import click

from .compose_helpers import (bootstrap_relay_tool, bootstrap_test_organization, get_test_ids,
                              new_test_context, provision_all_services, remove_all_test_contexts,
                              start_load_generator, stop_all_services, stop_load_generator)
from ..utils import get_rand_port


@click.command()
@click.option('-l', '--list-tests', 'list_tests', flag_value=True, default=False)
@click.option('-c', '--clear', 'clear', flag_value=True, default=False)
@click.option(
    '-i', '--test-id', 'test_id',
    type=click.INT, default=None,
    help='Continue specified test number.')
@click.pass_context
def cli(gctx, test_id, list_tests, clear):
    '''handle integration test runner state'''
    if (clear):
        remove_all_test_contexts()
        gctx.exit(0)

    if (list_tests):
        test_ids = get_test_ids()
        click.echo(', '.join([str(i) for i in sorted(test_ids)]))
        gctx.exit(0)

    if test_id is None:
        # create new test context
        click.echo('creating new test context!')
        test_id = new_test_context()
        click.echo('test context created!')

        click.echo('provisioning collection server!')
        click.echo('provisioning crypto server!')
        click.echo('provisioning load generator!')
        crypto_port = get_rand_port()
        provision_all_services(test_id, crypto_port)
        click.echo('crypto server instance ready!')
        click.echo('collection server instance ready!')

        # create new user/org
        click.echo('creating test organization!')
        organization_info = bootstrap_test_organization(test_id)
        click.echo('created test organization!')
        click.echo(organization_info)

        click.echo('configuring relay instance!')
        bootstrap_relay_tool(test_id, crypto_port, organization_info)
        click.echo('relay service started!')

        click.echo('starting load_generator service!')
        c_id = start_load_generator(test_id, organization_info)
        click.echo('load_generator service started!')

        click.echo('waiting for 50 seconds!')  # ~ 60 users , 300 emails (needs to be async)
        time.sleep(50)
        stop_load_generator(test_id, c_id)
        click.echo('load_generator service stopped!')

        # get server_state state

        click.echo('stopping all services!')
        stop_all_services(test_id)

        # expect_results(server_state, i)

    else:
        pass
        # NOTE: this needs collection server container to keep state
        # crypto_port = 0
        # sp_env = MergeDicts(p_env, {
        #     'COMPOSE_PROJECT_NAME': str(test_id),
        #     'CRYPTO_PORT': str(crypto_port)
        # })
        # click.echo('starting all services!')
        # subprocess.check_call(
        #     ['docker-compose', 'up', '-d'],
        #     cwd=TEST_RUNNER_ROOT, env=sp_env)

        # click.echo('starting load_generator service!')
        # p = subprocess.Popen(
        #     ['docker-compose', 'run', '--rm', '-d', 'load_generator', '-u', organization_info['admin_id']],
        #     stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT,
        #     env=MergeDicts(sp_env, {'NEW_MEMBER': str(5), 'NEW_EMAIL': str(1)}))
        # c_id = p.stdout.read().strip()
        # assert p.wait() == 0
        # click.echo('load_generator service started!')

        # click.pause('Press any button to stop test run ...')

        # p = subprocess.Popen(
        #     ['docker', 'stop', c_id],
        #     stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)
        # assert p.stdout.read().strip() == c_id
        # assert p.wait() == 0
        # click.echo('load_generator service stopped!')

        # click.echo('stopping all services!')
        # subprocess.check_call(
        #     ['docker-compose', 'stop'], cwd=TEST_RUNNER_ROOT, env=sp_env)
