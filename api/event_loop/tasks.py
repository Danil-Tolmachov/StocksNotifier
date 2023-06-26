import asyncio
from functools import wraps
from pymongo import collection

from services.checkers import AbstractChecker
from services.exceptions import ConfigurationError
from services.exceptions import DiscardedAction
from event_loop.utils import check_for_changes, endless_task
from event_loop.mongo import checker_types as checker_types_collection
from event_loop.mongo import subscription_types as subscription_collection
from event_loop.mongo import delivery_types as delivery_collection
    

def accept_action(message):
    warning_message = 'Some users might loose their checkers if you delete/move or change their checker class. \nDo you wand to proceed? Y/N : '
    if input(f'Delete/move actions detected in {message}. ' + warning_message) in ['Y', 'y']:
        pass
    else:
        raise DiscardedAction()
        return
    


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


def load_checkers(collection: collection) -> list[AbstractChecker]:
    pass

async def save_new_checker(collection: collection, checker) -> None:
    pass


@endless_task(delay=2)
async def append_checkers(collection: collection, list_obj: list, new_checkers: list) -> None:
    for checker in new_checkers:
        await save_new_checker(collection, checker)
        list_obj.append(checker)

@endless_task(delay=5)
async def pass_checkers(checkers: list[AbstractChecker]):
    for checker in checkers:
        if not checker.check():
            continue

        checker.subscription.send()
