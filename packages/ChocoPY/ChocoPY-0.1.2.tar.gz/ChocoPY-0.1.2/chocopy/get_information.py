from flask import request


def get_message():
    text = request.json['userRequest']['utterance']
    return text
