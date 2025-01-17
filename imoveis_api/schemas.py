from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
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
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PropertyList(BaseModel):
    properties: list[PropertyPublic]
