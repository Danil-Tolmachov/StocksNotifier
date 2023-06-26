import asyncio
import sys
import os.path
sys.path.append(os.path.curdir.split('api')[0])

from tasks import append_checkers, pass_checkers, initiate_settings, load_checkers
from mongo import checker_instances, checker_types, subscription_types, delivery_types



async def main():
    initiate_settings()
    #checkers = load_checkers()
    
    tasks = [
        #append_checkers(checker_instances, checkers, []),
        #pass_checkers(checkers),
    ]

    await asyncio.gather(*tasks)
        

if __name__ == '__main__':
    asyncio.run(main())
