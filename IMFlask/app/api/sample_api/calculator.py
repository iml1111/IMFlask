"""
Calculator API
"""
from flask import abort
from flask_validation_extended import Validator, Query
from flask_validation_extended import ValidationRule
from app.api.response import response_200, bad_request
from app.api.sample_api import sample_api as api
from app.api.decorator import timer
from controller import calculator, log


@api.route('/add')
@Validator(bad_request)
@timer
def add_api(
    a=Query(int),
    b=Query(int)
):
    return response_200(calculator.add(a, b))


@api.route('/subtract')
@Validator(bad_request)
@timer
def subtract_api(
    a=Query(int),
    b=Query(int)
):
    return response_200(calculator.subtract(a, b))


@api.route('/multiply')
@Validator(bad_request)
@timer
def multiply_api(
    a=Query(int),
    b=Query(int)
):
    return response_200(calculator.multiply(a, b))


class NotZero(ValidationRule):

    def invalid_str(self):
        return "Must Not be Zero."

    def is_valid(self, data) -> bool:
        return data != 0


@api.route('/divide')
@Validator(bad_request)
@timer
def divide_api(
    a=Query(int),
    b=Query(int, rules=NotZero())
):
    return response_200(calculator.divide(a, b))