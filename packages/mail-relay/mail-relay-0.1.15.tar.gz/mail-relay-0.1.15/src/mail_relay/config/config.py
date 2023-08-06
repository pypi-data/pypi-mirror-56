class SMTPConfig(object):
    def __init__(self, host, port, username, password, send_to_user, use_tls=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.send_to_user = send_to_user

    def to_json(self):
        return {
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'use_tls': self.use_tls,
            'send_to_user': self.send_to_user
        }


class IMAPConfig(object):
    def __init__(self, host, port, username, password, use_tls=False):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def to_json(self):
        return {
            'host': self.host,
            'port': self.port,
            'username': self.username,
            'password': self.password,
            'use_tls': self.use_tls
        }


class CSConfig(object):
    def __init__(self, host, port, use_tls=False):
        self.host = host
        self.port = port
        self.use_tls = use_tls

    @property
    def http(self):
        return u'{}://{}{}'.format(
            'https' if self.use_tls else 'http',
            self.host,
            '' if self.port == 80 else ':{}'.format(self.port))

    @property
    def ws(self):
        return u'{}://{}{}'.format(
            'wss' if self.use_tls else 'ws',
            self.host,
            '' if self.port == 80 else ':{}'.format(self.port))

    def to_json(self):
        return {
            'host': self.host,
            'port': self.port,
            'use_tls': self.use_tls
        }


class VolumeConfig(object):
    def __init__(self, path):
        self.path = path

    def to_json(self):
        return {'path': self.path}


class Config(object):
    def __init__(self, cs, smtp=None, imap=None, volume=None):
        if len([1 for c in (smtp, imap, volume,) if c is None]) != 2:
            raise ValueError('more than one config provided')
        self.smtp = smtp
        self.imap = imap
        self.cs = cs
        self.volume = volume

    @classmethod
    def from_yaml(cls, yaml_file):
        from pvHelpers.utils import read_yaml_config

        y = read_yaml_config(yaml_file)
        return cls.from_json(y)

    @classmethod
    def from_json(cls, j):
        cs, s, i, v = j['cs'], j.get('smtp'), j.get('imap'), j.get('volume')
        s = None if s is None else \
            SMTPConfig(s['host'], s['port'], s['username'], s['password'], s['send_to_user'], s['use_tls'])
        i = None if i is None else \
            IMAPConfig(i['host'], i['port'], i['username'], i['password'], i['use_tls'])
        v = None if v is None else \
            VolumeConfig(v['path'])

        return cls(
            CSConfig(cs['host'], cs['port'], cs['use_tls']), smtp=s, imap=i, volume=v)

    def __repr__(self):
        return str(self.to_json())

    def to_json(self):
        return {
            'cs': self.cs.to_json(),
            'smtp': self.smtp and self.smtp.to_json(),
            'imap': self.imap and self.imap.to_json(),
            'volume': self.volume and self.volume.to_json()
        }
