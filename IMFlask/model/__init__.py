"""
Application Model
"""
from flask import Flask
from controller import log
from config import APP_NAME


def register_connection_pool(app: Flask):
    pass

def init_app(config):
    """Model Init Function"""
    log.warning('No DB Initialized.')