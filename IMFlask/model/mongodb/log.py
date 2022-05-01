from datetime import datetime
from pymongo import IndexModel, DESCENDING, ASCENDING
from .base import Model


class Log(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return [
            IndexModel([('created_at', ASCENDING)])
        ]

    @property
    def schema(self) -> dict:
        return {
            'ipv4': None,
            'url': None,
            'method': None,
            'params': None,
            'status_code': None,
            'created_at': datetime.now(),
            '__version__': self.VERSION,
        }

    def insert_log(self, document):
        self.col.insert_one(self.schemize(document))

    def get_log(self, _skip: int, _limit: int):
        return (
            self.col.find(
                {}, self.p(all=True)
            )
            .sort([('created_at', DESCENDING)])
            .skip(_skip)
            .limit(_limit)
        )