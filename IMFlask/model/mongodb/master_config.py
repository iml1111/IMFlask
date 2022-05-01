from datetime import datetime
from .base import Model


class MasterConfig(Model):

    VERSION = 1

    @property
    def index(self) -> list:
        return []

    @property
    def schema(self) -> dict:
        return {
            'config_type': None,
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
            '__version__': self.VERSION,
        }

    def get_author(self):
        return self.col.find_one(
            {'config_type': 'author'},
            {
                '_id': 1,
                'config_type': 1,
                '__author__': 1,
                'created_at': 1,
                'updated_at': 1,
            }
        )

    def insert_author(self, author: str):
        document = self.schemize({
            'config_type': 'author',
            '__author__': author
        })
        self.col.update_one(
            {'config_type':'author'},
            {'$set': document},
            upsert=True
        )

    def change_author(self, author: str):
        self.col.update_one(
            {'config_type': 'author'},
            {
                '$set': {
                    '__author__': author,
                    'updated_at': datetime.now()
                }
            }
        )