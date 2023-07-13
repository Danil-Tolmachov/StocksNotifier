from typing import Optional
from pydantic import BaseModel, EmailStr, fields, validator
from re import match


class UserForm(BaseModel):
    id: Optional[int]

    username: str
    password: str

    email: EmailStr
    phone: str

    consumer_id: int # Id of company/delevoper related to user
    external_id: int # User id that consumer uses in their own DBs

    @validator('id')
    def validate_id(cls, id_value):
        if id_value <= 0:
            raise ValueError('id must be greater than zero')
        
        return id_value
    
    @validator('phone')
    def validate_phone(cls, phone_value):
        phone_pattern = r'^\d{10,13}$'
        if not match(phone_pattern, phone_value):
            raise ValueError('Invalid phone format')

        return phone_value
    

class DeveloperForm(BaseModel):
    id: Optional[int]

    username: str
    password: str

    users: Optional[list]
    template: Optional[None]
