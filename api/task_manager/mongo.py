from pymongo import MongoClient

from settings import MONGO_URL

client = MongoClient(MONGO_URL, 27017)

db = client['checkers_db']

checker_types = db['checker_types']
delivery_types = db['delivery_types']
subscription_types = db['subsctiption_types']
checker_instances = db['checkers']


checker_instances_example = [
    {
        'id': 1,
        'checker_type': 2,
        'dict': {
            'last_price': 110
        },
        'delivery_type': 1,
        'subscription_type': 1,
        'ticker': 'AAPL',
        'subscriber': 1,
        'active': True,
    },
    {
        'id': 2,
        'checker_type': 3,
        'dict': {
            'last_price': 110
        },
        'delivery_type': 1,
        'subscription_type': 1,
        'subscription_dict': {},
        'ticker': 'AAPL',
        'subscriber': [1, 2, 3],
        'active': True,
    },
    {
        'id': 3,
        'checker_type': 1,
        'dict': {
            'last_price': 110
        },
        'delivery_type': 1,
        'subscription_type': 1,
        'subscription_dict': {},
        'ticker': 'AAPL',
        'subscriber': 3,
        'active': True,
    },
]
