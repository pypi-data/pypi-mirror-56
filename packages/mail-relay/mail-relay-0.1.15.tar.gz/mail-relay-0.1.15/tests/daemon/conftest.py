from mail_relay.daemon.state import State
from mail_relay.store.handlers import (update_config,
                                       write_exporter, write_user,
                                       write_user_key)
import pytest


@pytest.fixture()
def get_state(get_store, unit_config):
    def _new_state(user):
        store = get_store()
        write_user_key(user.user_id, user.account_version, user.user_key, store)
        write_user(user, store)
        write_exporter(user.user_id, user.account_version, store)
        update_config(unit_config, store)
        return State(store)

    return _new_state
