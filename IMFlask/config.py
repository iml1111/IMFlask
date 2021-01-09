'''
Flask Application Config
'''
import os
from logging.config import dictConfig

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    '''공통 Config'''
    JWT_SECRET_KEY = os.environ.get('FLASK_JWT_SECRET_KEY')
    # test only
    TEST_ACCESS_TOKEN = os.environ.get('FLASK_TEST_ACCESS_TOKEN')
    ADMIN_ID = os.environ.get('FLASK_ADMIN_ID', "iml")
    ADMIN_PW = os.environ.get('FLASK_ADMIN_PW', "iml")

    # DB_PROXY: basic, mysql, mongodb, redis, all
    DB_PROXY = os.environ.get('FLASK_DB_PROXY')

    if DB_PROXY in ['mysql', 'all']:
        MYSQL_URI = os.environ.get('FLASK_MYSQL_URI')
    if DB_PROXY in ['mongodb', 'all']:
        MONGO_URI = os.environ.get('FLASK_MONGO_URI')
        MONGO_DB_NAME = os.environ.get('FLASK_MONGO_DB_NAME')
    if DB_PROXY == ['reids', 'all']:
        REDIS_HOST = os.environ.get('FLASK_REDIS_HOST')
        REDIS_PORT = os.environ.get('FLASK_REDIS_PORT')
        REDIS_PW = os.environ.get('FLASK_REDIS_PW')

    ALLOWED_EXTENSION = {'txt', 'docs', 'md', 'hwp', 'ppt', 'pptx'}
    SLOW_API_TIME = 0.5

    @staticmethod
    def init_app(app):
        '''전역 init_app 함수'''


class TestingConfig(Config):
    '''Test 전용 Config'''
    DEBUG = True
    TESTING = True


class DevelopmentConfig(Config):
    '''개발 환경 전용 Config'''
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    ''' 상용환경 전용 Config'''
    DEBUG = False
    TESTING = False

    @staticmethod
    def init_app(app):
        '''로거 등록 및 설정'''
        dictConfig({
            'version': 1,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                }
            },
            'handlers': {
                'file': {
                    'level': 'INFO',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': './server_error.log',
                    'maxBytes': 1024 * 1024 * 5,
                    'backupCount': 5,
                    'formatter': 'default',
                },
            },
            'root': {
                'level': 'INFO',
                'handlers': ['file']
            }
        })


config = {
    'development':DevelopmentConfig,
    'production':ProductionConfig,
    'testing':TestingConfig,

    'default':DevelopmentConfig,
}
