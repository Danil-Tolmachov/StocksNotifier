from fastapi import APIRouter, Form, Response
from starlette import status

from services.api.auth import create_tokens, authenticate
from services.api.models import User, Developer


router = APIRouter(
        prefix='/auth', 
        tags=['auth',]
    )


@router.post('/developer/register')
def register_developer(username: str = Form(), password: str = Form()):
    obj = Developer.objects.create(username=username, password=password)
    return Response(status_code=status.HTTP_201_CREATED)

@router.post('/user/register')
def register_user(username: str = Form(), password: str = Form()):
    obj = User.objects.create(username=username, password=password)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post('/developer/login')
def login_developer(username: str = Form(), password: str = Form()):
    dev = authenticate(username, password, is_developer=True)

    if dev is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    return Response(create_tokens(dev), status_code=status.HTTP_200_OK)

@router.post('/user/login')
def login_user(username: str = Form(), password: str = Form()):
    user = authenticate(username, password, is_developer=False)

    if user is None:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    return create_tokens(user)


@router.delete('/developer')
def delete_developer():
    pass

@router.delete('/user')
def delete_user():
    pass
