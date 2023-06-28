from functools import wraps
from datetime import datetime, timedelta, date
import asyncio

from services.exceptions import DiscardedAction


def endless_task(delay: int):
    def decorator(func):
        """
        Decorator function that creates an endless task that repeatedly calls a coroutine function.

        Args:
        delay: int
            The delay in seconds between each execution of the coroutine function.

        Example usage:
        @endless_task(2)
        async def my_task():
            print("Executing my_task...")
            # Do some asynchronous work
        """
        @wraps(func)
        async def loop(*args, **kwargs):
            while True:
                await func(*args, **kwargs)
                await asyncio.sleep(delay)

        return loop
    return decorator


def super_len(obj):
    """
    Function to determine the length of a cursor in pymongo.

    Args:
    obj: pymongo.cursor.Cursor
        The cursor object for which the length needs to be determined.

    Returns:
    int
        The number of elements in the cursor.

    Example usage:
    cursor = collection.find()
    length = super_len(cursor)
    print(length)

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

def serialize(dic: dict):
    pass_list = [int, str, list, dict, set, None, datetime, timedelta]
    remove_list = []
    copy = dic.copy()

    for key, item in dic.items():

        if item.__class__ not in pass_list:
            remove_list.append(key)
            
    for key in reversed(remove_list):
        copy.pop(key)

    return copy
