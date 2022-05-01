"""
Template Example API
"""
from flask import Blueprint, render_template

template = Blueprint('template', __name__)


@template.route('/')
def index():
    return render_template('index.html')