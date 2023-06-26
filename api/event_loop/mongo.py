from pymongo import MongoClient
import pickle

client = MongoClient('mongodb://root:test@localhost', 27017)

db = client['checkers_db']

checker_types = db['checker_types']
delivery_types = db['delivery_types']
subscription_types = db['subsctiption_types']
checker_instances = db['checkers']


checker_instances_example = [
    {
        'id': 1,
        'checker_type': 2,
        'delivery_type': 1,
        'subscription_type': 1,
        'ticker': 'AAPL',
        'subscriber': 1,
    },
    {
        'id': 2,
        'checker_type': 3,
        'delivery_type': 1,
        'subscription_type': 1,
        'ticker': 'AAPL',
        'subscriber': [1, 2, 3],
    },
    {
        'id': 3,
        'checker_type': 2,
        'delivery_type': 1,
        'subscription_type': 1,
        'ticker': 'AAPL',
        'subscriber': 3,
    },
]
