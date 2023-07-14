from fastapi import Header, HTTPException
from starlette import status

from services.api.auth import authenticate_token


def get_auth(Authorization: str = Header()):

    if len(Authorization.split()) < 2:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication bearer')

    if Authorization.split()[0] == 'token':
        token = Authorization.split()[1]

        if len(token) < 15:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user = authenticate_token(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return user
