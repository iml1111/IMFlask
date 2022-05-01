"""
API Main Decorator
"""
import json
from functools import wraps
from time import time
from flask import current_app, g, Response
from controller import log
from config import config


def timer(func):
    """API Timer"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        process_time = time()
        result = func(*args, **kwargs)
        g.process_time = time() - process_time

        if current_app.config['DEBUG']:
            if config.TIMER_OUTPUT == 'response':
                if isinstance(result, Response):
                    data = json.loads(result.get_data())
                    data['process_time'] = g.process_time
                    result.set_data(json.dumps(data))
                elif isinstance(result, tuple):
                    result[0]['process_time'] = g.process_time
                else:
                    result['process_time'] = g.process_time
            elif config.TIMER_OUTPUT == 'log':
                log.info(f"process_time: {g.process_time}")

        return result
    return wrapper