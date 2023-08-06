from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from flubber.middleware.loader import MiddlewareLoader


class FlubberApp(Flask):
    def __init__(self, *args, **kwargs):
        self.settings = None
        super(FlubberApp, self).__init__(__name__, *args, **kwargs)

        # TODO: Add proxy count from settings
        self.wsgi_app = ProxyFix(self.wsgi_app)
        self.load_settings()

    def load_settings(self):
        from flubber.contrib import settings

        self.settings = settings.load()


def create_app():
    app = FlubberApp()
    MiddlewareLoader(app)
    return app
