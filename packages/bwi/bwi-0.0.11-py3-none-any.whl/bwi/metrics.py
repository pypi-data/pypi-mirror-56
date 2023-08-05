import os
from datetime import datetime
from bwi._queue_sender import RabbitMQConnection


def _generate_message(metric_type: str, name: str, val: float):
    RabbitMQConnection().send_to_queue("metrics",
                                       {'type': metric_type,
                                        'metric_name': name,
                                        'value': val,
                                        'timestamp': datetime.timestamp(
                                            datetime.now())})
    return "Message sended"


def store(metric_name: str, value: float):
    """
    For a given metric, store a value inside Graphite.

    We send this value to a dedicated queue, which will do the saving in
    graphite

    We store the value if we are on the BWI Infra, else, we display it.
    :param metric_name: the name of the metric
    :param value: the value of the current action
    """
    if os.environ.get('BWI_INFRA') is not None:
        _generate_message('value', metric_name, value)
    else:
        print(metric_name, value)
