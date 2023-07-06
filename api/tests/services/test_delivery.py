import pytest
from datetime import datetime
from freezegun import freeze_time

from fixtures import get_checker, get_subscription


@pytest.mark.asyncio
@freeze_time('2023-06-28 20:20:20')
async def test_testing_delivery(get_checker):
    checker = get_checker
    
    with freeze_time('2023-07-29 20:21:20'):
        assert checker.send('test_user') == True
