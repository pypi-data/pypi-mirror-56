import os
import random

from mail_relay.config import Config, VolumeConfig
from mail_relay.daemon.state import State
from mail_relay.mail.mail_state import MailState
from mail_relay.store.handlers import (update_config, update_user_mail_state,
                                       write_exporter, write_user,
                                       write_user_key)
from pvHelpers.utils import randUnicode
import pytest

from ..utils import create_test_account, test_local_user


@pytest.mark.integration
def key_rotatation_test(cs_client, integration_config, store):
    # needs exporter
    with pytest.raises(KeyError):
        State(store)

    user = create_test_account(cs_client)

    write_user_key(user.user_id, user.account_version, user.user_key, store)
    write_user(user, store)

    # needs exporter
    with pytest.raises(KeyError):
        State(store)

    write_exporter(user.user_id, user.account_version, store)

    # needs config
    with pytest.raises(AttributeError):
        State(store)

    update_config(integration_config, store)
    state = State(store)
    assert len(state.local_users) == 2
    assert state.local_users[(user.account_version, user.user_id)].device.key == user.device.key

    state.rotate_device_key(user.user_id, user.account_version)

    assert state.local_users[(user.account_version, user.user_id)].device.key.key_version == \
        user.device.key.key_version + 1
    assert state.local_users[(user.account_version, user.user_id)].user_key == user.user_key

    # TODO: add test for intermittend rotation and handling of `401`


def relay_mime_test(get_state, tmpdir_factory):
    user = test_local_user()
    state = get_state(user)
    rev_id = random.randint(0, 999999999)
    update_user_mail_state(
        user.user_id, user.account_version, MailState(rev_id), state.store_path)

    for r in [rev_id, rev_id - 1]:
        err = state.relay_mime(user.user_id, user.account_version, randUnicode(), r, randUnicode())
        assert isinstance(err, ValueError)

    server_id = randUnicode()
    mime = randUnicode()
    export_path = os.path.abspath(str(tmpdir_factory.mktemp('export')))
    state.config = Config(state.config.cs, volume=VolumeConfig(export_path))

    err = state.relay_mime(user.user_id, user.account_version, server_id, rev_id + 1, mime)
    assert err is None
    assert state.get_members_last_rev_id(user.user_id, user.account_version) == rev_id + 1

    # check volume
    user_dir = os.path.join(export_path, user.user_id.lower())
    filename = os.path.join(
        os.path.join(export_path, user.user_id.lower()),
        server_id.lower()) + '.eml'

    assert os.path.isdir(user_dir)
    with open(filename) as f:
        assert f.read() == mime
