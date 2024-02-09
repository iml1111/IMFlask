"""
Application Factory Module
"""
import json
from typing import Any, Union
from datetime import datetime
from flask import Flask
from flask.json.provider import JSONProvider
from app import api
from app.api.template import template as template_bp
from app.api.error_handler import error_handler as error_bp
from app.api.sample_api import sample_api as sample_api_bp
from model import register_connection_pool


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%m:%S")
        else:
            return super().default(obj)


class CustomJsonProvider(JSONProvider):

    def dumps(self, obj: Any, **kwargs: Any) -> str:
        return json.dumps(obj, **kwargs, cls=CustomJSONEncoder)

    def loads(self, s: Union[str, bytes], **kwargs: Any) -> Any:
        return json.loads(s, **kwargs)


def create_flask_app(config):
    app = Flask(
        import_name=__name__,
        instance_relative_config=True,
        static_url_path='/',
        static_folder='asset/',
        template_folder='asset/'
    )

    app.json = CustomJsonProvider(app)
    app.config.from_object(config)
    config.init_app(app)
    api.init_app(app)
    register_connection_pool(app)

    app.register_blueprint(error_bp)
    app.register_blueprint(template_bp)
    app.register_blueprint(sample_api_bp, url_prefix='/sample/')

    return app
