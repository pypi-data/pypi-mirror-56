from flask import jsonify


def set_response(keys: str, value = None) -> jsonify:
    """
    set_response function is set response easily

    Example : return set_response("ID", "res")

    :param keys: key
    :param value: value
    :return: Response that type is json

    -----------------------------------------------

    If you want to show a data in chat,
    you must setting in 'bot response'

    Scenario -> Create text style response
    => {{#webhook.keys}}

    """

    return jsonify({
        keys: value
    })