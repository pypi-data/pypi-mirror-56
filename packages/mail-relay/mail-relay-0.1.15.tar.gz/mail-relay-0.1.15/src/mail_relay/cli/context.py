import click
from pvHelpers.cs_client import BackendClient


class Context(object):
    def __init__(self, store, config):
        self.store = store
        self.config = config
        if self.config:
            self.cs_client = BackendClient()
            self.cs_client.init(self.config.cs.http)
        else:
            self.config = None


ctx = click.make_pass_decorator(Context)
