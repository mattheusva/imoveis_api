from typing import Optional

import phonenumbers
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    CRECI: Optional[str] = None

    @field_validator('phone')
    def validate_phone(cls, value):
        if value is None:
            return value
        try:
            phone_obj = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_obj):
                raise ValueError('Invalid phone number')
            return phonenumbers.format_number(
                phone_obj, phonenumbers.PhoneNumberFormat.E164
            )
        except phonenumbers.NumberParseException:
            raise ValueError('Invalid phone number')


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    phone: Optional[str] = None
    CRECI: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class PropertySchema(BaseModel):
    type: str
    area: float
    rooms: int
    bathrooms: int
    garages: int
    value: float
    transaction: str
    description: Optional[str]
    address: str
    city: str
    state: str
    status: str


class PropertyPublic(PropertySchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PropertyList(BaseModel):
    properties: list[PropertyPublic]


class Token(BaseModel):
    access_token: str
    token_type: str
