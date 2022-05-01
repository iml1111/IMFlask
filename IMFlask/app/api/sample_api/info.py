"""
Get API
"""
from flask import g, jsonify, current_app
from flask_validation_extended import Json, Validator
from app.api.response import response_200, bad_request, created
from app.api.sample_api import sample_api as api
from app.api.decorator import timer


@api.route('/author')
@timer
def get_author_api():
    return response_200('IML')