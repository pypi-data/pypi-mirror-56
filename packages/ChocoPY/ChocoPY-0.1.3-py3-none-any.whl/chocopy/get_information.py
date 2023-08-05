from flask import request


def get_message() -> str:
    """
    The get_message function is to receive message
    from Kakao chatbot's request

    user_message = get_message()
    :return: The Message that is parsed request

    """
    text = request.json['userRequest']['utterance']
    return text

def get_block() -> str:
    """
    The get_intent function is to receive block name
    from kakao chatbot's request

    block_name = get_block()

    :return: Block name
    """
    block = request.json['userRequest']['block']['name']
    return block

