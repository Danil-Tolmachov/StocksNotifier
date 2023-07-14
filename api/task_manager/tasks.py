import asyncio
from types import CoroutineType

from services.abstractions import AbstractChecker
from services.checkers import *
from services.subscriptions import *
from services.tickers import *
from services.delivery import *
from services.exceptions import ConfigurationError, DiscardedAction

from task_manager.utils import check_for_changes, serialize_dict, accept_action, to_datetime_dict_objects
from task_manager.mongo import checker_instances
from task_manager.mongo import checker_types as checker_types_collection
from task_manager.mongo import subscription_types as subscription_collection
from task_manager.mongo import delivery_types as delivery_collection
from task_manager.celery_app import app




@app.on_after_configure.connect
def at_start(sender, **kwargs):
    # Initiate classes schema from settings.py
    initiate_settings()

    # Initiate checkers from db
    checkers = init_checkers(checker_instances)
    globals().update({'checkers_to_append': []})
    globals().update({'checkers': checkers})

    sender.add_periodic_task(10.0, append_checkers.s(), name='Append new checkers')
    sender.add_periodic_task(10.0, pass_checkers.s(), name='Pass through checkers')



@app.task
def append_checkers() -> None:
    """
        Asynchronously appends checkers to the collection, and adds to the global 'checkers' list.
        Uses 'checkers_to_append' global list instance.
    """
    collection = checker_instances
    global checkers
    global checkers_to_append

    async def func():
        async with ClientSession() as session:
            for checker in checkers_to_append: 
                save_new_checker(collection, checker)

                if type(checker) == CoroutineType:
                    await checker.update(session)
                else:
                    checker.update(session)

                checkers.append(checker)
    return asyncio.run(func())

@app.task
def pass_checkers() -> None:
    """
        Asynchronously checks and updates the checkers(if check method returns True).
        Uses checker.subscription.send() if the check is successful.
    """
    
    async def func():
        tasks = []

        async def check(checker, session):
                    if type(checker) == CoroutineType:
                        if await checker.check(session):
                            await checker.update(session)
                            checker.subscription.send()
                    else:
                        if checker.check(session):
                            checker.update(session)
                            checker.subscription.send()

        async with ClientSession() as session:
            for checker in checkers:
                tasks.append(check(checker, session))

            await asyncio.gather(*tasks)

    return asyncio.run(func())
                        

@app.task
def initiate_settings():
    """
        Initializes the classes settings by validating and applying the provided configurations.

        Raises:
            ConfigurationError: If any of the required settings (checker_types, subscription_types, delivery_types) are missing or empty.
            DiscardedAction: If a change is detected but is discarded due to an accept action.
    """
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


@app.task
def load_checker(record: dict) -> AbstractChecker:
    """
        Loads and initializes a checker object based on the provided record dict.

        Args:
            record (dict): The record containing information about the checker.

        Returns:
            AbstractChecker: The initialized checker object.
    """

    #
    # Record example:
    #
    # {
    #     'id': 1,
    #     'checker_type': 2,
    #     'dict': {
    #         'last_price': 110
    #     },
    #     'delivery_type': 1,
    #     'subscription_type': 1,
    #     'ticker': 'AAPL',
    #     'subscriber': 1,
    #     'active': True,
    # },
    #
    
    subscription_class: type = None
    checker_class: type = None

    local = {}

    # Get delivery class
    try:
        delivery = delivery_collection.find({'id': record.get('delivery_type')})[0]['class']
    except IndexError:
        broken_id = record['delivery_type']
        print(f"Record with non-exist delivery class detected: id={broken_id}, skiping...")
        return None
    exec(f'delivery_class = {delivery}', globals(), local)
    delivery_class: type = local['delivery_class']

    # Get subscription class
    try:
        sub = subscription_collection.find({'id': record['subscription_type']})[0]['class']
    except IndexError:
        broken_id = record.get('subscription_type')
        print(f"Record with non-exist subscription class detected: id={broken_id}, skiping...")
        return None
    exec(f"subscription_class = {sub}", globals(), local)
    subscription_class: type = local['subscription_class']

    # Get checker class
    try:
        checker = checker_types_collection.find({'id': record['checker_type']})[0]['class']
    except IndexError:
        broken_id = record.get('checker_type')
        print(f"Record with non-exist checker class detected: id={broken_id}, skiping...")
        return None
    exec(f'checker_class = {checker}', globals(), local)
    checker_class: type = local['checker_class']

    # Create subscription object
    subscription_obj = subscription_class(Ticker(record.get('ticker')), delivery=delivery_class(), id=record['subscriber'])
    checker_obj = checker_class(subscription_obj)

    # Create checker object
    checker_obj.__dict__.update(to_datetime_dict_objects(record['checker_dict']))
    checker_obj.subscription.__dict__.update(to_datetime_dict_objects(record['subscription_dict']))

    return checker_obj


def init_checkers(collection) -> list[AbstractChecker]:
    """
        Loads and initializes a checkers list object based on the provided records.
    
        Args:
            collection (MongoDB collection): The records containing information about the checkers.
    
        Returns:
            list[AbstractChecker]: The initialized checkers list object.
    """
    return_list = []
    cursor = collection.find({})

    for raw_checker in cursor:
        return_list.append(load_checker(raw_checker))

    return return_list


def serialize_checker(collection, checker_obj: AbstractChecker) -> dict:
    """
        Serializes the provided checker object into a dictionary for storage in the given collection.

        Args:
            collection: The collection where the serialized checker will be stored.
            checker_obj (AbstractChecker): The checker object to serialize.

        Returns:
            dict: The serialized checker object as a dictionary.

        Raises:
            ValueError: If the checker_obj or its related classes are not included or enabled in the settings.py.
    """
     
    try:
        checker_name = type(checker_obj).__name__
        checker_id = checker_types_collection.find({'class': checker_name})[0]['id']
    except IndexError:
        raise ValueError(f"You can't use class '{checker_name}', include it to 'Active classes' of settings")

    try:
        subscription_name = type(checker_obj.subscription).__name__

        if subscription_name == 'ABCMeta':
            raise ValueError(f'Setup {type(checker_obj).__name__}.subscription, before saving the checker')
        
        subscription_id = subscription_collection.find({'class': subscription_name})[0]['id']
    except IndexError:
        raise ValueError(f"You can't use class '{subscription_name}', enable it in 'Active classes' of settings")
        
    try:
        delivery_name = type(checker_obj.subscription.delivery).__name__

        if delivery_name == 'ABCMeta':
            raise ValueError(f'Setup {type(checker_obj).__name__}.delivery, before saving the checker')

        delivery_id = delivery_collection.find({'class': delivery_name})[0]['id']
    except IndexError:
        raise ValueError(f"You can't use class '{delivery_name}', enable it in the 'Active classes' of settings")
    
    try:
        obj_id = collection.find().sort([('id', -1)]).limit(1)[0]['id'] + 1
    except IndexError:
        obj_id = 1

    checker_dict = checker_obj.__dict__
    checker_dict = serialize_dict(checker_dict)
    
    subscription_dict = checker_obj.__dict__['subscription'].__dict__
    subscription_dict = serialize_dict(subscription_dict)

    result = {
        'id': obj_id,
        'checker_type': checker_id,
        'checker_dict': checker_dict,
        'delivery_type': delivery_id,
        'subscription_type': subscription_id,
        'subscription_dict': subscription_dict,
        'ticker': str(checker_obj.subscription.ticker),
        'subscriber': checker_obj.subscription.subscriber,
        'active': True,
    }
    return result

@app.task
def save_new_checker(collection, checker: AbstractChecker) -> None:
    """
        Serializes and saves the provided checker object into the given collection.
    
        Args:
            collection: The collection where the checker will be saved.
            checker (AbstractChecker): The checker object to save.
    """
    serialized = serialize_checker(collection, checker)
    collection.insert_one(serialized)
