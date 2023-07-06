from fastapi import APIRouter


router = APIRouter()


@router.get('/checkers')
def get_available_checker_types():
    pass

@router.post('/user/subscribe')
def subscribe_user(id: int, ticker: str, type: str):
    pass

@router.post('/users/subscribe')
def subscribe_users(ids: list[int], ticker: str):
    pass

@router.post('/user/unsubscribe')
def unsubscribe_user(subscription_id: int):
    pass

@router.post('/users/unsubscribe')
def unsubscribe_users(subscription_ids: list[int]):
    pass
