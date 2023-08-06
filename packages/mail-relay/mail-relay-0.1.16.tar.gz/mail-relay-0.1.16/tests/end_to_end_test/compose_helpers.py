import os
import random
import shutil
import subprocess
import time

import click
from pvHelpers.utils import jloads, MergeDicts

from ..utils import crypto_send_user_key

TEST_RUNNER_ROOT = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(TEST_RUNNER_ROOT, '.test_data')
TEST_PREFIX = 'test_'
CONFIGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'configs')
P_ENV = os.environ.copy()


def test_dir(test_id):
    return os.path.join(TEST_DIR, '{}{}'.format(TEST_PREFIX, test_id))


def get_test_ids():
    return [int(d.split('_')[1]) for d in os.listdir(TEST_DIR) if d.startswith(TEST_PREFIX)]


def new_test_context():
    existing_test_ids = get_test_ids()
    next_id = max([-1] + existing_test_ids) + 1
    next_dir = test_dir(next_id)
    os.mkdir(next_dir)
    # create volumes
    for v in ['crypto', 'export', 'relay']:
        os.mkdir(os.path.join(next_dir, v))

    # set config file for relay tool
    shutil.copyfile(
        os.path.join(CONFIGS_DIR, 'volume.test.yml'),
        os.path.join(next_dir, 'relay', 'config.yml'))

    return next_id


def remove_all_test_contexts():
    for i in get_test_ids():
        subprocess.check_call(
            ['docker-compose', 'down', '-v'], cwd=TEST_RUNNER_ROOT,
            env=MergeDicts(P_ENV, {'COMPOSE_PROJECT_NAME': str(i), 'CRYPTO_PORT': str(0)}))

        shutil.rmtree(test_dir(i))


def provision_all_services(test_id, crypto_port):
    sp_env = MergeDicts(P_ENV, {
        'COMPOSE_PROJECT_NAME': str(test_id),
        'CRYPTO_PORT': str(crypto_port)
    })
    subprocess.check_call(
        ['docker-compose', 'up', '-d', '--build', '--force-recreate'],
        cwd=TEST_RUNNER_ROOT, env=sp_env)
    # idle some time for services to become reachable
    time.sleep(15)


def stop_all_services(test_id):
    sp_env = MergeDicts(P_ENV, {
        'COMPOSE_PROJECT_NAME': str(test_id),
        'CRYPTO_PORT': str(0)
    })
    subprocess.check_call(
        ['docker-compose', 'stop'], cwd=TEST_RUNNER_ROOT, env=sp_env)


def bootstrap_test_organization(test_id):
    sp_env = MergeDicts(P_ENV, {
        'COMPOSE_PROJECT_NAME': str(test_id),
        'CRYPTO_PORT': str(0)
    })
    p = subprocess.Popen(
        ['docker-compose', 'run', '--rm', 'load_generator', '-c'],
        stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)
    # print p.stdout.read()
    assert p.wait() == 0
    return jloads(unicode(p.stdout.read()))


def bootstrap_relay_tool(test_id, crypto_port, organization_info):
    sp_env = MergeDicts(P_ENV, {
        'COMPOSE_PROJECT_NAME': str(test_id),
        'CRYPTO_PORT': str(crypto_port)
    })
    click.echo('migrating database!')
    subprocess.check_call(
        ['docker-compose', 'run', '--rm', 'relay', 'migrate'],
        cwd=TEST_RUNNER_ROOT, env=sp_env)
    click.echo('relay database migrated!')

    click.echo('configuring relay instance!')
    subprocess.check_call(
        ['docker-compose', 'run', '--rm', 'relay', 'config', '-c', './data/config.yml'],
        cwd=TEST_RUNNER_ROOT, env=sp_env)
    click.echo('relay configuration saved!')

    click.echo('configuring relay exporter!')
    p = subprocess.Popen(
        ['docker-compose', 'run', '--rm', 'relay', 'config', 'exporter', organization_info['admin_id']],
        stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)
    send_pin_handle = crypto_send_user_key('127.0.0.1', crypto_port, organization_info['admin_id'])
    time.sleep(3)
    p.stdout.readline()  # skip just info line
    pin = p.stdout.readline().split('pin: ')[1].strip()
    send_pin_handle(pin)
    assert p.wait() == 0
    click.echo('relay exporter {} configured!'.format(organization_info['admin_id']))

    click.echo('configuring approvers!')
    for a in random.sample(organization_info['approvers'], organization_info['optionals_required']):
        p = subprocess.Popen(
            ['docker-compose', 'run', '--rm', 'relay', 'config', 'approver', a['user_id']],
            stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)
        send_pin_handle = crypto_send_user_key('127.0.0.1', crypto_port, a['user_id'])
        time.sleep(3)
        p.stdout.readline()  # skip just info line
        pin = p.stdout.readline().split('pin: ')[1].strip()
        send_pin_handle(pin)
        assert p.wait() == 0
        click.echo('relay approver {} configured!'.format(a['user_id']))

    click.echo('starting relay service!')
    subprocess.check_call(
        ['docker-compose', 'start', 'relay'],
        stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)


def start_load_generator(test_id, organization_info):
    sp_env = MergeDicts(P_ENV, {
        'COMPOSE_PROJECT_NAME': str(test_id),
        'CRYPTO_PORT': str(0)
    })
    p = subprocess.Popen(
        ['docker-compose', 'run', '--rm', '-d', 'load_generator', '-u', organization_info['admin_id']],
        stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT,
        env=MergeDicts(sp_env, {'NEW_MEMBER': str(5), 'NEW_EMAIL': str(1)}))
    c_id = p.stdout.read().strip()
    assert p.wait() == 0
    return c_id


def stop_load_generator(test_id, c_id):
    sp_env = MergeDicts(P_ENV, {
        'COMPOSE_PROJECT_NAME': str(test_id),
        'CRYPTO_PORT': str(0)
    })
    p = subprocess.Popen(
        ['docker', 'stop', c_id],
        stdout=subprocess.PIPE, cwd=TEST_RUNNER_ROOT, env=sp_env)
    assert p.stdout.read().strip() == c_id
    assert p.wait() == 0
