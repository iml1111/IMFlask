'''
MySQL Management Modules and Models
'''
import pymysql
from sqlalchemy.engine.url import make_url
from flask import g, current_app
from werkzeug.security import generate_password_hash
from app.models.mysql.tables import tables

def get_mysql_cur(store_g=True):
    '''
    Open DB Cursor Connection

    Params
    -------
    store_g : if True, store to Flask Global Object g.
    '''
    uri = current_app.config['MYSQL_URI']
    uri = make_url(uri)
    mysql_cur = pymysql.connect(
            host=uri.host,
            port=uri.port,
            user=uri.username,
            passwd=uri.password,
            db=uri.database,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

    if store_g:
        g.mysql_cur = mysql_cur

    return mysql_cur


def close_mysql_cur():
    '''
    Close DB Cursor Connection
    '''
    mysql_cur = g.pop('mysql_cur', None)
    if mysql_cur:
        mysql_cur.close()


def mysql_init():
    '''db-init in MySQL'''
    uri = current_app.config['MYSQL_URI']
    uri = make_url(uri)
    conn = pymysql.connect(
            host=uri.host,
            port=uri.port,
            user=uri.username,
            passwd=uri.password,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)

    with conn.cursor() as cur:
        # Create DB
        sql = '''
            CREATE DATABASE IF NOT EXISTS imldb default CHARACTER SET UTF8;
        '''
        cur.execute(sql)
    conn.commit()
    conn.select_db("imldb")

    with conn.cursor() as cur:
        # Create Tables
        for sql in tables:
            cur.execute(sql)
    conn.commit()

    with conn.cursor() as cur:
        # Create Test Records
        sql = '''
            INSERT INTO master_config(author) VALUES ('IML');
        '''
        cur.execute(sql)
        # Create ADMIN Data
        sql = '''
            INSERT IGNORE INTO user(id, pw) VALUES (%s, %s);
        '''
        sql = sql.format(admin_id=current_app.config['ADMIN_ID'])
        cur.execute(sql, 
            (
                current_app.config['ADMIN_ID'], 
                generate_password_hash(current_app.config['ADMIN_PW'])
            )
        )

    conn.commit()
    conn.close()
