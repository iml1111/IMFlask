"""
Application Model
"""
from flask import Flask
from config import APP_NAME
from model import mongodb


def register_connection_pool(app: Flask):
    app.db = mongodb.get_cursor()


def init_app(config):
    """Model Init Function"""

    # MongoDB Init
    initializer = mongodb.ModelInitializer()
    initializer.init_model()
    print("[%s] MongoDB Initialization Completed." % APP_NAME)