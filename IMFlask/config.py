'''
Application Config Setting
'''
import os
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv(verbose=True)

APP_NAME = "IMFlask"
BASEDIR = os.path.abspath(os.path.dirname(__file__))
FLASK_CONFIG = os.getenv('FLASK_CONFIG') or 'development'


class Config:
    '''General Config'''
    SLOW_API_TIME = 0.5
    API_LOGGING = False
    JSON_AS_ASCII = False
    SECRET_KEY = "top-secret"
    MONGODB_URI = os.environ[APP_NAME + "_MONGODB_URI"]
    MONGODB_NAME = os.environ[APP_NAME + "_MONGODB_NAME"]
    # API 타이머 출력 경로 (response, log, none)
    TIMER_OUTPUT = os.getenv('TIMER_OUTPUT', 'response')

    @staticmethod
    def init_app(app):
        pass

if FLASK_CONFIG == 'development':
    class AppConfig(Config):
        DEBUG = True
        TESTING = False

elif FLASK_CONFIG == 'production':
    class AppConfig(Config):
        DEBUG = False
        TESTING = False

        @staticmethod
        def init_app(app):
            '''File Logger Sample'''
            dictConfig({
                'version': 1,
                'formatters': {
                    'default': {
                        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                    }
                },
                'handlers': {
                    'file': {
                        'level': 'WARNING',
                        'class': 'logging.handlers.RotatingFileHandler',
                        'filename': os.getenv(APP_NAME + '_ERROR_LOG_PATH') or './server.error.log',
                        'maxBytes': 1024 * 1024 * 5,
                        'backupCount': 5,
                        'formatter': 'default',
                    },
                },
                'root': {
                    'level': 'WARNING',
                    'handlers': ['file']
                }
            })
else:
    raise Exception("Flask Config not Selected.")

config = AppConfig

class TestConfig(Config):
    DEBUG = True
    TESTING = True

if __name__ == '__main__':
    pass