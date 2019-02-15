class WQApiEndpoint(object):
    def __init__(self, client):
        self.client = client

    def do_post(self, *args, **kwargs):
        return self.client.do_post(*args, **kwargs)

    def do_get(self, *args, **kwargs):
        return self.client.do_get(*args, **kwargs)
