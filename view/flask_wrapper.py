from view.endpoint_handler import EndpointHandler


class FlaskAppWrapper(object):

    def __init__(self, app, **configs):
        self.app = app
        self.configs(**configs)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], defaults=None, *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name,
                              EndpointHandler(handler), methods=methods, defaults=defaults, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)
