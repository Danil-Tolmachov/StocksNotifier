from fastapi import APIRouter, Query


router = APIRouter()


@router.get('/user/{external_id}')
def get_user(external_id: int):
    pass

@router.get('/users')
def get_users():
    pass


@router.post('/user')
def create_users(users: list[dict], multi = Query()):
    pass

@router.post('/user')
def create_user():
    pass


@router.patch('/user/')
def update_user(email: str = Query(), phone: str = Query()):
    pass


@router.delete('/user/{id}')
def delete_user():
    pass

@router.delete('/users')
def delete_users(ids: list[int]):
    pass
