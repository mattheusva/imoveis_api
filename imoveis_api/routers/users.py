from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from imoveis_api.database import get_session
from imoveis_api.models import User
from imoveis_api.schemas import Message, UserList, UserPublic, UserSchema
from imoveis_api.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])


# Endpoint para criar user
@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(
    user: UserSchema, session: AsyncSession = Depends(get_session)
):
    db_user = await session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username,
        password=hashed_password,
        email=user.email,
        phone=user.phone,
        CRECI=user.CRECI,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


# Endpoint para ler users
@router.get('/', response_model=UserList)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
):
    result = await session.scalars(select(User).offset(skip).limit(limit))
    users = result.all()

    return {'users': users}


# Endpoint para atualizar user
@router.put('/{user_id}', response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        current_user.phone = user.phone
        current_user.CRECI = user.CRECI
        await session.commit()
        await session.refresh(current_user)

        return current_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )


# Endpoint para deletar user
@router.delete('/{user_id}', response_model=Message)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    await session.delete(current_user)
    await session.commit()

    return {'message': 'User deleted'}
