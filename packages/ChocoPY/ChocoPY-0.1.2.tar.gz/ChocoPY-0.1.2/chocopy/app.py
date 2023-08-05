from flask import Flask, jsonify

from chocopy.exceptions import UnknownKeyError


class ChocoPY:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self._default_configuration(app)
        self._error_handler(app)

    @staticmethod
    def _default_configuration(app: Flask):
        app.config['ENV'] = 'ChatBot Server'
        app.config['DEBUG'] = False
        app.config.setdefault('BOT_ERROR_MESSAGE_KEY', "error")

    @staticmethod
    def _error_handler(app: Flask):
        @app.errorhandler(UnknownKeyError)
        def handle_Unknown_key_error(request, e):
            return jsonify({
                app.config.BOT_ERROR_MESSAGE_KEY: 'Unknown keys'
            })

