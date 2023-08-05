from flask import jsonify


def set_response(keys: str, value = None) -> jsonify:
    """
    set_response function is set response easily

    return set_response("ID", "res")

    :param keys: key
    :param value: value
    :return: Response that type is json
    """

    jsonify({
        keys: value
    })