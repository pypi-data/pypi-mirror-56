from .key import KeyBucket


class TempDeviceKeyBycket(KeyBucket):
    NAME = u'temp_device_key'
    CURRENT_VERSION = 0

    @staticmethod
    def key(user_id, account_version, key_version):
        return '{};{}'.format(account_version, user_id.lower())
