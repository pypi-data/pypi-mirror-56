import time

import pytest

from .compose_helpers import (bootstrap_relay_tool, bootstrap_test_organization,
                              new_test_context, provision_all_services,
                              start_load_generator, stop_all_services, stop_load_generator)
from ..utils import get_rand_port


@pytest.mark.end2end
def end2end_test():
    test_id = new_test_context()
    crypto_port = get_rand_port()
    provision_all_services(test_id, crypto_port)
    organization_info = bootstrap_test_organization(test_id)
    bootstrap_relay_tool(test_id, crypto_port, organization_info)
    c_id = start_load_generator(test_id, organization_info)

    time.sleep(50)
    stop_load_generator(test_id, c_id)

    # TODO: get server_state state

    stop_all_services(test_id)

    # TODO: expect_results(server_state, i)
