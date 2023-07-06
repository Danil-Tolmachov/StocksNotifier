from fastapi import APIRouter, Query


router = APIRouter()


@router.get('/user/{external_id}')
def get_user(external_id: int):
    pass

@router.get('/users')
def get_users():
    pass

@router.get('/subscription/{id}')
def get_subscription_object(id: int):
    pass

@router.get('/subscriptions')
def get_subscription_objects():
    pass


@router.post('/user')
def create_user():
    pass

@router.post('/users')
def create_users(users: list[dict]):
    pass


@router.patch('/user/')
def update_user(phone: str = Query()):
    pass


@router.delete('/user/{id}')
def delete_user():
    pass

@router.delete('/users')
def delete_users(ids: list[int]):
    pass
