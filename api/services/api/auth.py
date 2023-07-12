from datetime import timedelta, datetime
from jose import jwt
from typing import Tuple, Union

from services.exceptions import InvalidToken
from services.api.models import User, Developer 
from services.api.utils import validate_password
from mongo import developer_instances, user_instances
from settings import settings


secret = settings.SECRET_KEY
algorithm = settings.JWT_ALGORITHM
access_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
refresh_expire = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN)


#
# Create tokens
#

def create_access_token(user: Union[User, Developer], expire_delta: timedelta = access_expire) -> Tuple[str, datetime]:
    expiration = datetime.utcnow() + expire_delta
    payload = {
        'id': user.id,
        'is_developer': True if isinstance(user.__class__, Developer) else False,
        'username': user.username,
        'password': user.password,
        'exp': expiration,
    }
    return jwt.encode(payload, secret, algorithm), expiration

def create_refresh_token(access_token: str, expire_delta: timedelta = refresh_expire) -> Tuple[str, datetime]:
    obj = jwt.decode(access_token, secret, algorithm)
    obj.pop('exp')

    # Validate token
    if obj is None:
        raise InvalidToken()

    expiration = datetime.utcnow() + expire_delta
    payload = {
        'exp': expiration,
        **obj
    }

    return jwt.encode(payload, secret, algorithm), expiration


#
# Authentication and authorization
#

def authenticate_token(token: str) -> Union[User, Developer]:
    data = jwt.decode(token)
    id = data.get('id')
    is_developer = data.get('is_developer')

    # Validate token
    if id is None or is_developer is None:
        raise InvalidToken()

    # Get User/Developer object
    try:
        if is_developer:
            return Developer.objects.find({'id': id})
        else:
            return User.objects.get({'_id': id})
    except Exception:
        return None

def authenticate(username: str, password: str, is_developer: bool = True) -> Union[User, Developer]:

    # Get User/Developer object
    try:
        if is_developer:
            obj = Developer.objects.get({'username': username})
        else:
            obj = User.objects.get({'username': username})
    except:
        return None
    
    # Check password
    if validate_password(password, obj.password):
        return obj
    else:
        return None

def authorization(username: str, password: str, is_developer: bool = True) -> dict:
    obj = authenticate(username, password, is_developer)

    if obj is None:
        return None

    # Tokens expiration
    access_expire_delta: timedelta = access_expire
    refresh_expire_delta: timedelta = refresh_expire
    
    # Create tokens
    access_token, access_exp = create_access_token(obj, expire_delta=access_expire_delta)
    refresh_token, refresh_exp = create_refresh_token(access_token, expire_delta=refresh_expire_delta)

    result = {
        'access': {
            'token': access_token,
            'exp': access_exp,
        },
        'refresh': {
            'token': refresh_token,
            'exp': refresh_exp,
        },
    }
    return result
