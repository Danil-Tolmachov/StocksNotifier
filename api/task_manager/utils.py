from functools import wraps
from datetime import datetime, timedelta
from re import match
import asyncio

from services.exceptions import DiscardedAction


def endless_task(delay: int):
    """
        Decorator function that creates an endless task that repeatedly calls a coroutine function.
        Args:
        delay: int
            The delay in seconds between each execution of the coroutine function.
    """
    def decorator(func):
        @wraps(func)
        async def loop(*args, **kwargs):
            
            while True:
                await func(*args, **kwargs)
                await asyncio.sleep(delay)

        return loop
    return decorator


def super_len(obj) -> int:
    """
    Function to determine the length of a cursor.
    """
    i = 0
    for j in obj:
        i += 1
    return i


def accept_action(message):
    warning_message = 'Some users might loose their checkers if you delete/move or change their checker class. \nDo you wand to proceed? Y/N : '
    if input(f'Delete/move actions detected in {message}. ' + warning_message) in ['Y', 'y']:
        pass
    else:
        raise DiscardedAction()
        return


def check_for_changes(new_collection, old_collection) -> bool:
    """
        Function to check for changes between two collections in pymongo.

        Args:
        new_collection: pymongo.cursor.Cursor
            The cursor object representing the new collection.
        old_collection: pymongo.cursor.Cursor
            The cursor object representing the old collection.

        Returns:
        bool
            True if there are changes (elements removed) between the collections, False otherwise.

        Example usage:
        new_cursor = new_collection.find()
        old_cursor = old_collection.find()
        has_changes = check_for_changes(new_cursor, old_cursor)
        if has_changes:
            print("Changes detected.")
        else:
            print("No changes detected.")
    """
    removal = False
    buff = []
    
    for old in old_collection:
        del old['_id']
        buff.append(old)

    for instance in buff:
        if instance not in new_collection:
            removal = True
    return removal

def serialize_dict(_dict: dict) -> dict:
    """
    Removes dict values that can't be serialized with Mongo.

    Arguments:
    - _dict (dict): The original dictionary.

    Returns:
    - dict: The serialized dictionary.

    Serialization conditions:
    - Values of types in pass_list remain unchanged.
    - Values of type datetime are converted to string representation using the format '%Y-%m-%dT%H:%M:%S.%f'.
    """
    pass_list = [int, str, list, dict, set, None, datetime, timedelta]
    remove_list = []
    copy = _dict.copy()

    for key, item in _dict.items():

        if item.__class__ not in pass_list:
            remove_list.append(key)

        if isinstance(item.__class__, datetime):
            copy[key] = item.strftime('%Y-%m-%dT%H:%M:%S.%f')
            
    for key in reversed(remove_list):
        copy.pop(key)

    return copy

def to_datetime_dict_objects(_dict: dict) -> dict:
    """
    Converts string representations of datetime objects in a dictionary to datetime objects.

    Arguments:
    - _dict (dict): The input dictionary.

    Returns:
    - dict: The dictionary with datetime objects converted from string representations.
    """
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$'
    for key, item in _dict.items():
        if not isinstance(item, str):
            continue

        if match(pattern, item):
            _dict[key] = datetime.strptime(item, '%Y-%m-%dT%H:%M:%S.%f')
    return _dict
