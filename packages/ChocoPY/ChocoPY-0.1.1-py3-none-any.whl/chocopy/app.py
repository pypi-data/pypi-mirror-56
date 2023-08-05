from flask import Flask


class ChocoPY:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self._default_configuration(app)
        self._error_handler(app)

    @staticmethod
    def _default_configuration(app: Flask):
        app.config['host'] = '0.0.0.0'
        app.config['port'] = 5555
        app.config['debug'] = False

    @staticmethod
    def _error_handler(app: Flask):
        pass