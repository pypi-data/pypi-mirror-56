import logging
import os
from datetime import datetime
from bwi._queue_sender import RabbitMQConnection


logger = logging.getLogger('bwi_lib')
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
def _generate_message(level: str, message: str):
    current_timestamp = datetime.timestamp(datetime.now())
    RabbitMQConnection().send_to_internal_queue(
        queue_name=os.environ.get('BWI_LOGGING_QUEUE'),
        message={'level': level, 'message': message, 'timestamp': current_timestamp})
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
        logger.info(message)


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
        logger.info(message)


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
        logger.info(message)


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
        logger.info(message)


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
        logger.info(message)
