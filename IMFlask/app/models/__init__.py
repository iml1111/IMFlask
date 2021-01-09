'''
Flask Application Models
'''
import sys
from app.models.mysql import mysql_init
from app.models.mongodb import mongo_init
from app.models.redis import redis_init


def init_app(app):
    '''
    db-init cli command function
    '''
    if app.config['DB_PROXY'] in ['mysql', 'all']:
        mysql_init()
        sys.stdout.write("Mysql init ... OK" + "\n")
    
    if app.config['DB_PROXY'] in ['mongodb', 'all']:
        mongo_init()
        sys.stdout.write("MongoDB init ... OK" + "\n")

    if app.config['DB_PROXY'] in ['redis', 'all']:
        redis_init()
        sys.stdout.write("Redis init ... OK" + "\n")
