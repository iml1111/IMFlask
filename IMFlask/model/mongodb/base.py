from abc import ABCMeta
from datetime import datetime
from flask import _app_ctx_stack, current_app
from pymongo import MongoClient
from model.mongodb import get_cursor
from config import config


class Model(metaclass=ABCMeta):

    VERSION = 1

    def __init__(
        self,
        client: MongoClient = None,
        db_name: str = config.MONGODB_NAME
    ):
        if client is None and _app_ctx_stack.top is not None:
            client: MongoClient = current_app.db
        elif client is None:
            client: MongoClient = get_cursor()
        self.col = client[db_name][self.__class__.__name__]

    @property
    def index(self) -> list:
        """Get Index List"""
        return []

    @property
    def schema(self) -> dict:
        """Get default document format"""
        return {
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }

    def create_index(self) -> None:
        """Create indexes"""
        if self.index:
            self.col.create_indexes(self.index)

    def schemize(self, document: dict) -> dict:
        """Generate JSON scheme"""
        return {**self.schema, **document}

    def p(self, *args, all=False) -> dict:
        """projection shortcut method"""
        if not all:
            return {field: 1 for field in args}
        else:
            return {field: 1 for field in self.schema.keys()}
