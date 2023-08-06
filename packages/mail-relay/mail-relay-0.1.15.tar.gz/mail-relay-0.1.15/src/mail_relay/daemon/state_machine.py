import time

from pvHelpers.cs_client.utils import ExpiredDeviceKey, ExpiredUserKey
from pvHelpers.logger import g_log
import requests

from .mail_export_scheduler import MailExportScheduler


class StateMachine(object):
    def __init__(self, state):
        self._ctx = state

    def run_forever(self):
        while True:
            try:
                export_state, err = self._ctx.get_set_export_state()
                if err is not None:
                    g_log.error(err)
                    time.sleep(1)
                    continue

                # given valid `export_state` init export scheduler
                scheduler = MailExportScheduler(self._ctx)
                scheduler.run()
            except ExpiredDeviceKey as e:
                # g_log.exception(e.exception)
                g_log.info(u'rotating device key version {} for {}'.format(e.key_version, e.user_id))
                self._ctx.rotate_device_key(e.user_id, e.account_version)
            except ExpiredUserKey as e:
                # if failure for exporter we must terminate process
                pass
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 401:
                    # TODO: handle intermittent device key rotation
                    pass
                raise
            except Exception as e:
                g_log.exception(e)
                raise
            finally:
                time.sleep(0.5)
