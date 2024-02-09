import logging
from flask import current_app
from logging import Logger


class SingletonInstane:
  __instance = None

  @classmethod
  def __getInstance(cls):
    return cls.__instance

  @classmethod
  def instance(cls, *args, **kargs):
    cls.__instance = cls(*args, **kargs)
    cls.instance = cls.__getInstance
    return cls.__instance


class DefaultLogger(SingletonInstane):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s:%(levelname)s> %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)


def get_app_logger() -> Logger:
    try:
        logger = current_app.logger
    except RuntimeError:
        logger = DefaultLogger.instance().logger
    return logger


def info(*args):
    _log('INFO', *args)

def warning(*args):
    _log('WARNING', *args)


def _log(level: str, *args):
    desc = " ".join([str(i) for i in args])
    logger: Logger = get_app_logger()

    if level == 'INFO':
        logger.info(desc)
    elif level == 'WARNING':
        logger.warning(desc)
    else:
        raise RuntimeError('Undefined loglevel.')


if __name__ == '__main__':
    info('default log execute...')