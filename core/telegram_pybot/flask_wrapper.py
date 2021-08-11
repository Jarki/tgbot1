from flask import Flask, Response


class EndpointAction(object):

    def __init__(self, action):
        self.action = action
        self.response = Response(status=200, headers={})

    def __call__(self, *args):
        self.action()
        return self.response


class FlaskWrapper:
    def __init__(self, name):
        self.app = Flask(name)

    def run(self):
        self.app.run()

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=None):
        if methods is None:
            methods = ["GET"]

        self.app.add_url_rule(endpoint, endpoint_name, EndpointAction(handler), methods=methods)
