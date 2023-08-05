from flask import Flask, jsonify

from chocopy.exceptions import UnknownKeyError


class ChocoPY:
    def __init__(self, app=None):
        """
        ChocoPY is a development tool that makes Kakao's chatbot easy.
        Must use Flask framework because it runs on Flask applications

        app = Flask(__name__)
        ChocoPY(app)

        :param app: A Flask Application

        """

        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        """
        :param app: A Flask Application
        """

        self._default_configuration(app)
        self._error_handler(app)

    @staticmethod
    def _default_configuration(app: Flask):
        """
        Set the configuration
        :param app: A Flask Application
        """

        app.config['ENV'] = 'ChatBot Server'
        app.config['DEBUG'] = False
        app.config.setdefault('BOT_ERROR_MESSAGE_KEY', "error")

    @staticmethod
    def _error_handler(app: Flask):
        """
        Set the ChocoPY Error Handler in Flask Application
        :param app: A Flask Application
        :return: Response
        """

        @app.errorhandler(UnknownKeyError)
        def handle_Unknown_key_error(request, e):
            return jsonify({
                app.config.BOT_ERROR_MESSAGE_KEY: 'Unknown keys'
            })

