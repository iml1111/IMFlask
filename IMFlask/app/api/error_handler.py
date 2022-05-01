from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from app.api.response import not_found, bad_request

error_handler = Blueprint("error_handler", __name__)


@error_handler.app_errorhandler(400)
def bad_request_error(error: HTTPException):
    """400 Error Handler"""
    return bad_request(error.description)


@error_handler.app_errorhandler(404)
def not_found_error(error: HTTPException):
    """404 Error Handler"""
    return not_found


@error_handler.app_errorhandler(500)
def internal_server_error(error):
    """500 Error Handler (production only)"""
    return jsonify(msg=str(error)), 500