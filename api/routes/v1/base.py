from fastapi import APIRouter, Query


router = APIRouter()

@router.get('/user/fields')
def get_user_data_fields():
    pass

@router.get('/subscription/{id}')
def get_subscription_object(id: int):
    pass

@router.get('/subscription')
def get_subscription_objects():
    pass
