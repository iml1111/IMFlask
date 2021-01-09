'''
Auth API routes
'''
from flask import Blueprint, request, g
from app.api import input_check
from app.controllers.user_con import create_user
from app.controllers.user_con import signin
from app.api.decorators import (login_required,
                                admin_required,
                                login_optional,
                                timer)

auth = Blueprint('auth', __name__)


@auth.route("/signup", methods=['POST'])
def api_signup():
    '''회원가입 API'''
    data = request.get_json()
    input_check(data, 'user_id', str)
    input_check(data, 'user_pw', str)
    if create_user(g.mysql_cur,
                   data['user_id'],
                   data['user_pw']):
        return {"msg":"success"}
    return {"msg":"already user"}


@auth.route("/signin")
def api_signin():
    '''로그인 API'''
    data = request.get_json()
    input_check(data, 'user_id', str)
    input_check(data, 'user_pw', str)
    result = signin(g.mysql_cur,
                    data['user_id'],
                    data['user_pw'])
    if not result:
        return {'msg':'login Failed'}
    return {
        "msg":"success",
        "result":result
    }


@auth.route("/login_test")
@timer
@login_required
def api_login_test():
    '''로그인 테스트 API'''
    return {
        "msg": "success",
        "result": "Hello, " + str(g.user_id),
    }


@auth.route("/login_optional_test")
@timer
@login_optional
def api_login_optional_test():
    '''로그인 옵셔널 테스트 API'''
    return {
        "msg": "success",
        "result": "Hello, " + str(g.user_id),
    }


@auth.route("/admin_test")
@timer
@admin_required
def api_admin_test():
    '''관리자 테스트 API'''
    return {
        "msg": "success",
        "result": "Admin, " + str(g.user_id),
    }
