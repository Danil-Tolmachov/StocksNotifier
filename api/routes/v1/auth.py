from fastapi import APIRouter, Form, Response
from starlette import status

from services.api.auth import create_tokens, authenticate
from services.api.models import User, Developer
from services.api.forms import DeveloperForm, UserForm


router = APIRouter(
        prefix='/auth', 
        tags=['auth',]
    )


@router.post('/developer/register')
def register_developer(dev: DeveloperForm):
    obj = Developer.objects.create(username=dev.username, password=dev.password)
    return Response(status_code=status.HTTP_201_CREATED)

@router.post('/user/register')
def register_user(user: UserForm):
    obj = User.objects.create(username=user.username, password=user.password)
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


@router.delete('/developer/delete')
def delete_developer():
    pass
