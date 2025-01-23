from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    CRECI: Optional[str] = None


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
