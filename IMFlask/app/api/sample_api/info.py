"""
Get API
"""
from flask import g, jsonify, current_app
from flask_validation_extended import Json, Validator
from app.api.response import response_200, bad_request, created
from app.api.sample_api import sample_api as api
from app.api.decorator import timer
from model.mongodb import MasterConfig, Log


@api.route('/log')
@timer
def get_log_api():
    return response_200(list(Log().get_log(0, 10)))


@api.route('/author')
@timer
def get_author_api():
    return response_200(MasterConfig().get_author())


@api.route('/author', methods=['POST', 'PUT'])
@Validator(bad_request)
def change_author_api(
    name=Json(str)
):
    MasterConfig().change_author(name)
    return created


@api.route('/jsonify')
def get_jsonify_api():
    return jsonify(msg='성공!')