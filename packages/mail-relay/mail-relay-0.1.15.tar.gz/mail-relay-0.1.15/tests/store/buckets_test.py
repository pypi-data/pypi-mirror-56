import random

from mail_relay.config import Config, CSConfig, SMTPConfig, VolumeConfig
from mail_relay.daemon.export_state import ExportState
from mail_relay.daemon.helpers import export_groups_equal
from mail_relay.mail.mail_state import MailState
from mail_relay.store.handlers import (add_or_update_export_state, delete_user, read_config, read_export_state,
                                       read_temp_device_key, read_user_key, read_user_keys, read_user_mail_state,
                                       read_users, remove_records, update_config, update_user_info,
                                       update_user_mail_state, write_temp_device_key, write_user, write_user_key)
from pvHelpers.crypto import PVKeyFactory
from pvHelpers.request import ExportRequest
from pvHelpers.utils import CaseInsensitiveSet, jdumps, randUnicode
import pytest
import sqlalchemy.exc

from ..utils import rand_user_id, test_local_user, users_equal


def key_bucket_test(store):
    for _ in xrange(random.randint(0, 10)):
        test_user = rand_user_id()
        account_version = random.randint(0, 1000)
        key_version_count = random.randint(0, 40)
        for i in xrange(key_version_count):
            k = PVKeyFactory.newUserKey(i)
            write_user_key(test_user, account_version, k, store)
            k2 = read_user_key(test_user, account_version, i, store)
            assert k2 == k

        keys = read_user_keys(test_user, account_version, store)
        assert len(keys) == key_version_count


def temp_device_key_bucket_test(store):
    test_user = rand_user_id()
    account_version = random.randint(0, 1000)
    user_key = PVKeyFactory.newUserKey(0)
    write_user_key(test_user, account_version, user_key, store)

    device_key = PVKeyFactory.newUserKey(0)
    write_temp_device_key(test_user, account_version, device_key, store)

    assert device_key == read_temp_device_key(test_user, account_version, store)
    assert len(read_user_keys(test_user, account_version, store)) == 1
    assert user_key == read_user_key(test_user, account_version, 0, store)

    with pytest.raises(sqlalchemy.exc.IntegrityError):
        write_temp_device_key(test_user, account_version, device_key, store)


def user_bucket_test(store):
    test_users = []
    record_ids = []
    for _ in xrange(random.randint(1, 10)):
        test_users.append(test_local_user())
        record_ids.append(write_user(test_users[-1], store))

    users = read_users(store)
    for tu in test_users:
        assert users_equal(tu, users[(tu.account_version, tu.user_id)])

    u = test_users[0]
    d = PVKeyFactory.newUserKey(1)
    u.device.key = d
    update_user_info(u, store)
    assert read_users(store)[(u.account_version, u.user_id)].device.key == d
    delete_user(u.user_id, store)
    assert read_users(store).get((u.account_version, u.user_id)) is None
    update_user_info(u, store)
    assert read_users(store).get((u.account_version, u.user_id)) is None
    rid = write_user(u, store)
    assert read_users(store)[(u.account_version, u.user_id)] is not None

    assert len(read_users(store)) > 2
    remove_records(record_ids, store)
    assert len(read_users(store)) == 2
    remove_records([rid], store)
    assert len(read_users(store)) == 0


def config_bucket_test(store):
    config = read_config(store)
    assert config is None

    test_config = Config(
        CSConfig(randUnicode(10), random.randint(0, 55555), False),
        SMTPConfig(randUnicode(10), random.randint(0, 55555), randUnicode(10), randUnicode(10), rand_user_id(), False)
    )
    update_config(test_config, store)
    config = read_config(store)
    assert config.smtp.password == test_config.smtp.password

    test_config.smtp = None
    test_config.volume = VolumeConfig(randUnicode())
    rid = update_config(test_config, store)
    config2 = read_config(store)
    assert config2.smtp is None
    assert config2.volume.path == test_config.volume.path
    remove_records([rid], store)
    assert read_config(store) is None


def export_state_bucket_test(store):
    export_state = read_export_state(store)
    assert export_state is None

    # create dummy export
    req = {
        'user_id': rand_user_id(),
        'type': randUnicode(),
        'timestamp': randUnicode(),
        'expiration': randUnicode(),
        'device_id': randUnicode(),
        'data':  {'random': randUnicode()}
    }
    signature, serialized_req, req_id = randUnicode(), jdumps(req), randUnicode()
    test_group = {
        'approvers': [
            {'user_id': rand_user_id(), 'account_version': random.randint(0, 10000)},
            {'user_id': rand_user_id(), 'account_version': random.randint(0, 10000)},
            {'user_id': rand_user_id(), 'account_version': random.randint(0, 10000)}
        ],
        'optionals_required': 2
    }
    approvers_info = {
        rand_user_id(): {'approver_shards': {}, 'approver_signature': randUnicode()},
        rand_user_id(): {'approver_shards': {}, 'approver_signature': randUnicode()}
    }
    e = ExportState(
        ExportRequest(serialized_req, signature, req_id), test_group, approvers_info)

    add_or_update_export_state(e, store)
    export_state = read_export_state(store)
    assert export_state is not None
    assert export_state.request.serialized_req == serialized_req
    assert export_state.request.request_id == req_id
    assert export_groups_equal(export_state.export_group, test_group)
    assert CaseInsensitiveSet([(id_, i['approver_signature']) for id_, i in approvers_info.iteritems()]) == \
        CaseInsensitiveSet([(id_, s)for id_, s in export_state.approver_signatures.iteritems()])

    new_info = {rand_user_id(): {'approver_shards': {}, 'approver_signature': randUnicode()} for _ in xrange(10)}
    e = ExportState(
        ExportRequest(serialized_req, signature, req_id), test_group, new_info)

    add_or_update_export_state(e, store)
    new_state = read_export_state(store)
    assert new_state is not None
    assert new_state.request.serialized_req == serialized_req
    assert new_state.request.request_id == req_id
    assert export_groups_equal(new_state.export_group, test_group)
    assert CaseInsensitiveSet([(id_, i['approver_signature']) for id_, i in new_info.iteritems()]) == \
        CaseInsensitiveSet([(id_, s)for id_, s in new_state.approver_signatures.iteritems()])


def mail_state_bucket_test(store):
    for _ in xrange(random.randint(0, 50)):
        user_id = rand_user_id()
        account_version = random.randint(0, 99999999999)
        rev_id = random.randint(0, 99999999999)
        s = read_user_mail_state(user_id, account_version, store)
        assert s is None

        update_user_mail_state(user_id, account_version, MailState(rev_id), store)
        s = read_user_mail_state(user_id, account_version, store)
        assert rev_id == s.rev_id

        rev_id2 = random.randint(0, 99999999999)
        update_user_mail_state(user_id, account_version, MailState(rev_id2), store)
        s = read_user_mail_state(user_id, account_version, store)
        assert rev_id2 == s.rev_id
