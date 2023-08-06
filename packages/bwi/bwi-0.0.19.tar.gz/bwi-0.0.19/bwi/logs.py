import logging
import os
from datetime import datetime
from bwi._queue_sender import RabbitMQConnection


def _generate_message(level: str, message: str):
    RabbitMQConnection().send_to_internal_queue(
        os.environ.get('BWI_LOGGING_QUEUE'),
        {'level': level, 'message': message,
         'timestamp': datetime.timestamp(
             datetime.now())})
    return "Message sended"


def debug(message: str):
    """
    Log a message with debug level

    We send this message to a dedicated queue, which will do the saving in
    our log keeper

    We store the message if we are on the BWI Infra, else, we display it.
    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("debug", message)
    else:
        logging.info(message)


def info(message: str):
    """
    Log a message with info level

    We send this message to a dedicated queue, which will do the saving in
    our log keeper

    We store the message if we are on the BWI Infra, else, we display it.
    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("info", message)
    else:
        logging.info(message)


def warning(message: str):
    """
    Log a message with warning level

    We send this message to a dedicated queue, which will do the saving in
    our log keeper

    We store the message if we are on the BWI Infra, else, we display it.
    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("warning", message)
    else:
        logging.info(message)


def error(message: str):
    """
    Log a message with error level

    We send this message to a dedicated queue, which will do the saving in
    our log keeper

    We store the message if we are on the BWI Infra, else, we display it.
    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("error", message)
    else:
        logging.info(message)


def critical(message: str):
    """
    Log a message with critical level

    We send this message to a dedicated queue, which will do the saving in
    our log keeper

    We store the message if we are on the BWI Infra, else, we display it.
    :param message: the message to log
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message("critical", message)
    else:
        logging.info(message)
