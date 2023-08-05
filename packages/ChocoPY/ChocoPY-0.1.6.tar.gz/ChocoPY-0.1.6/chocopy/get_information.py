from flask import request


def get_message() -> str:
    """
    The get_message function is to receive message
    from request

    user_message = get_message()
    :return: The Message that is parsed request

    """
    text = request.json['userRequest']['utterance']
    return text

def get_block() -> str:
    """
    The get_intent function is to receive block name
    from request

    block_name = get_block()

    :return: Block name
    """
    block = request.json['userRequest']['block']['name']
    return block

def get_bot_name() -> str:
    """
    The get_bot_name function is to receive bot name
    from request

    :return:  Bot name used by the user
    """
    bot_name = request.json['bot']['name']
    return bot_name

def get_action_clientExtra() -> str or None:
    """
    The get_action_clientExtra function is to receive clientExtra

    :return: Client Extra
    """
    action_clientExtra = request.json['action']['clientExtra']
    return action_clientExtra


def get_intent_block_name() -> str:
    """
    The get_intent_block_name is to receive intent block name

    :return: Intent block name
    """
    intent_block_name = request.json['intent']['name']
    return intent_block_name


def get_timezone() -> str:
    """
    The get_timezone function is receive requests timezone

    :return: Timezone , Example : Asia/Seoul
    """
    timezone = request.json['userRequest']['timezone']
    return timezone


def get_user_id() -> str:
    """
    This function is receive User ID

    :return: User ID
    """
    user_id = request.json['userRequest']['type']
    return user_id

def get_params() -> dict:
    """
    This function is receive parameters
    parameter mean button that is run command or anything

    :return: Parameters
    """
    params = request.json['action']['params']
    return params


def get_detailParams() -> dict:
    """
    This function is receive detail parameters

    :return: Parameters
    """
    params = request.json['action']['detailParams']
    return params


