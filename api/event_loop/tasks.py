from functools import wraps
from pymongo import collection

from services.abstractions import AbstractChecker
from services.checkers import *
from services.subscriptions import *
from services.tickers import *
from services.delivery import *
from services.exceptions import ConfigurationError, DiscardedAction

from event_loop.utils import check_for_changes, endless_task, super_len, serialize, accept_action
from event_loop.mongo import checker_types as checker_types_collection
from event_loop.mongo import subscription_types as subscription_collection
from event_loop.mongo import delivery_types as delivery_collection


def initiate_settings():
    try:
        from settings import checker_types, subscription_types, delivery_types

        if checker_types == {}:
            raise ConfigurationError('checkers_types')
        if subscription_types == {}:
            raise ConfigurationError('subscription_types')
        if delivery_types == {}:
            raise ConfigurationError('delivery_types')
    except:
        raise ConfigurationError('checkers_types', 'subscription_types', 'delivery_types')
    
    try: 
        if check_for_changes(checker_types, checker_types_collection.find({})):
            accept_action('checker_types')
        if check_for_changes(subscription_types, subscription_collection.find({})):
            accept_action('subscription_types')
        if check_for_changes(delivery_types, delivery_collection.find({})):
            accept_action('delivery_types')
    except DiscardedAction:
        print('Discarded an action. Changes will not be applied.')
        print('Exiting...')
        exit()
    

    checker_types_collection.delete_many({})
    subscription_collection.delete_many({})
    delivery_collection.delete_many({})
    
    checker_types_collection.insert_many(checker_types)
    subscription_collection.insert_many(subscription_types)
    delivery_collection.insert_many(delivery_types)

async def load_checker(record: dict) -> bool:
    
    subscription_class: type = None
    checker_class: type = None

    local = {}

    try:
        delivery = delivery_collection.find({'id': record.get('delivery_type')})[0]['class']
    except IndexError:
        broken_id = record['delivery_type']
        print(f"Record with non-exist delivery class detected: id={broken_id}, skiping...")
        return False
    exec(f'delivery_class = {delivery}', globals(), local)
    delivery_class: type = local['delivery_class']

    try:
        sub = subscription_collection.find({'id': record['subscription_type']})[0]['class']
    except IndexError:
        broken_id = record.get('subscription_type')
        print(f"Record with non-exist subscription class detected: id={broken_id}, skiping...")
        return False
    exec(f"subscription_class = {sub}", globals(), local)
    subscription_class: type = local['subscription_class']

    try:
        checker = checker_types_collection.find({'id': record['checker_type']})[0]['class']
    except IndexError:
        broken_id = record.get('checker_type')
        print(f"Record with non-exist checker class detected: id={broken_id}, skiping...")
        return False
    exec(f'checker_class = {checker}', globals(), local)
    checker_class: type = local['checker_class']

    subscription_obj = subscription_class(Ticker(record.get('ticker')), delivery=delivery_class(), id=record['subscriber'])
    checker_obj = await checker_class.create(subscription_obj)

    checker_obj.__dict__.update(record['checker_dict'])
    checker_obj.subscription.__dict__.update(record['subscription_dict'])

    return checker_obj

async def load_checkers(collection: collection) -> list[AbstractChecker]:
    return_list = []
    cursor = collection.find({})

    for raw_checker in cursor:
        return_list.append(await load_checker(raw_checker))

    return return_list

def save_new_checker(collection: collection, checker: AbstractChecker) -> bool:
     
    try:
        checker_name = type(checker).__name__
        checker_id = checker_types_collection.find({'class': checker_name})[0]['id']
    except IndexError:
        raise ValueError(f"You can't use class '{checker_name}', include it to 'Active classes' of settings")

    try:
        subscription_name = type(checker.subscription).__name__

        if subscription_name == 'ABCMeta':
            raise ValueError(f'Setup {type(checker).__name__}.subscription, before saving the checker')
        
        subscription_id = subscription_collection.find({'class': subscription_name})[0]['id']
    except IndexError:
        raise ValueError(f"You can't use class '{subscription_name}', enable it in 'Active classes' of settings")
        
    try:
        delivery_name = type(checker.subscription.delivery).__name__

        if delivery_name == 'ABCMeta':
            raise ValueError(f'Setup {type(checker).__name__}.delivery, before saving the checker')

        delivery_id = delivery_collection.find({'class': delivery_name})[0]['id']
    except IndexError:
        raise ValueError(f"You can't use class '{delivery_name}', enable it in the 'Active classes' of settings")
    
    try:
        obj_id = collection.find().sort([('id', -1)]).limit(1)[0]['id'] + 1
    except IndexError:
        obj_id = 1

    checker_dict = checker.__dict__
    checker_dict = serialize(checker_dict)
    
    subscription_dict = checker.__dict__['subscription'].__dict__
    subscription_dict = serialize(subscription_dict)

    obj = {
        'id': obj_id,
        'checker_type': checker_id,
        'checker_dict': checker_dict,
        'delivery_type': delivery_id,
        'subscription_type': subscription_id,
        'subscription_dict': subscription_dict,
        'ticker': str(checker.subscription.ticker),
        'subscriber': checker.subscription.subscriber,
        'active': True,
    }
    collection.insert_one(obj)  


@endless_task(delay=2)
async def append_checkers(collection: collection, list_obj: list, new_checkers: list) -> None:
    for checker in new_checkers:
        save_new_checker(collection, checker)
        list_obj.append(checker)


@endless_task(delay=5)
async def pass_checkers(checkers: list[AbstractChecker]):
    for checker in checkers:
        if not checker.check():
            continue

        checker.subscription.send()
