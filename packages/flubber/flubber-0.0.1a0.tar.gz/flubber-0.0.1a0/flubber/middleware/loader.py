from importlib import import_module
from typing import List


class MiddlewareLoader:
    def __init__(self, app: object, middlewares: List[object] = []):
        self.app: object = app
        self.middlewares: List[str] = []
        self.load_middleware()

    def get_middleware_from_settings(self):
        self.middlewares: List[str] = self.app.settings.middlewares
        return self.middlewares

    def load_middleware(self):
        self.get_middleware_from_settings()

        for middleware in self.middlewares:
            module: object = import_module(middleware)
            module.init_app(self.app)
