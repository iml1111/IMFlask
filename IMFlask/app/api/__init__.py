'''
API rquest handler and Util
'''
from flask import abort, g, current_app, request
from app.models.mysql import get_mysql_cur, close_mysql_cur
from app.models.mongodb import get_mongo_cur, close_mongo_cur
from app.models.redis import get_redis_cur, close_redis_cur


def init_app(app):
    '''api request handler 초기화'''
    
    @app.before_first_request
    def before_first_request():
        '''맨 처음 리퀘스트가 오기 전에'''

    @app.before_request
    def before_request():
        '''HTTP 요청이 들어올때 마다'''
        if app.config['DB_PROXY'] in ['mysql', 'all']:
            get_mysql_cur(store_g=True)
        if app.config['DB_PROXY'] in ['mongodb', 'all']:
            get_mongo_cur(store_g=True)
        if app.config['DB_PROXY'] in ['redis', 'all']:
            get_redis_cur(store_g=True)

    @app.after_request
    def after_request(response):
        '''HTTP 요청이 끝나고 브라우저에 응답하기 전에'''
        if 'process_time' in g and \
        g.process_time >= current_app.config['SLOW_API_TIME']:
            log_str = "\n!!! SLOW API DETECTED !!! \n" + \
                      "ip: " + request.remote_addr + "\n" + \
                      "url: " + request.full_path + "\n" + \
                      "input_json: " + str(request.get_json()) + "\n" + \
                      "slow time: " + str(g.process_time) + "\n"
            app.logger.warning(log_str)
        return response

    @app.teardown_request
    def teardown_request(exception):
        '''HTTP 요청이 끝나고 브라우저에 응답하기 전에'''
        if app.config['DB_PROXY'] in ['mysql', 'all']:
            close_mysql_cur()
        if app.config['DB_PROXY'] in ['mongodb', 'all']:
            close_mongo_cur()
        if app.config['DB_PROXY'] in ['redis', 'all']:
            close_redis_cur()

    @app.teardown_appcontext
    def teardown_appcontext(exception):
        '''app context가 종료되기 전에'''


def input_check(data, key, value_type):
    '''input 파라미터 인자 검증 함수'''
    if key not in data:
        abort(400, description="'%s' not in data." % key)
    if not isinstance(data[key], value_type):
        abort(400, description="'%s' must be '%s' type." % (key, str(value_type)))
