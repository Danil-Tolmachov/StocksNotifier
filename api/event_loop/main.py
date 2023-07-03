import asyncio
import sys
import os.path
sys.path.append(os.path.curdir.split('api')[0])

from tasks import append_checkers, pass_checkers, initiate_settings, init_checkers
from mongo import checker_instances, checker_types, subscription_types, delivery_types
from messages import consume_messages



async def main():
    initiate_settings()
    checkers = init_checkers(checker_instances)

    checkers_to_append = []

    tasks = [
        append_checkers(checker_instances, checkers, checkers_to_append),
        pass_checkers(checkers),
        consume_messages(checkers, checkers_to_append),
    ]

    await asyncio.gather(*tasks)
        

if __name__ == '__main__':
    asyncio.run(main())
