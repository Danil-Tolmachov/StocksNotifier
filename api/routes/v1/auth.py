from fastapi import APIRouter


router = APIRouter()

@router.post('/register')
def register_consumer():
    pass

@router.post('/login')
def login_consumer() -> str:
    pass


@router.delete('/account')
def delete_consumer():
    pass
