from datetime import datetime
from controller.util import get_fake

class Mock:

    @staticmethod
    def get_log(_skip, _limit):
        fake = get_fake()
        results = [
            {
                'ipv4': fake.ipv4(),
                'url': fake.uri(),
                'method': fake.random_element(elements=('GET', 'POST', 'PUT')),
                'params': fake.text(max_nb_chars=200),
                'status_code': fake.random_element(elements=(200, 400, 404)),
                'created_at': datetime.now()
            } for _ in range(_limit)
        ]
        return list(sorted(results, key=lambda x: x['created_at'], reverse=True))

    @staticmethod
    def get_author():
        return {
            'config_type': 'author',
            '__author__': 'IML',
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }

