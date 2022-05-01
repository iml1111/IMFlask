"""
Sample API Module Package
"""
from flask import Blueprint

sample_api = Blueprint('sample_api', __name__)

from . import calculator, info