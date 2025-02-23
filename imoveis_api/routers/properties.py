from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from imoveis_api.database import get_session
from imoveis_api.models import Property, User
from imoveis_api.schemas import (
    Message,
    PropertyFilter,
    PropertyList,
    PropertyPublic,
    PropertySchema,
)
from imoveis_api.security import get_current_user

router = APIRouter(prefix='/properties', tags=['properties'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=PropertyPublic
)
def create_property(
    property: PropertySchema,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    new_property = Property(**property.model_dump())
    session.add(new_property)
    session.commit()
    session.refresh(new_property)

    return new_property


@router.get('/', response_model=PropertyList)
def list_properties(
    session: Session = Depends(get_session),
    filter: PropertyFilter = Query(),
):
    query = select(Property)

    # Filtros básicos
    if filter.state:
        query = query.filter(Property.state == filter.state)

    if filter.city:
        query = query.filter(Property.city.ilike(f'%{filter.city}%'))

    if filter.transaction:
        query = query.filter(Property.transaction == filter.transaction.value)

    if filter.type:
        query = query.filter(Property.type == filter.type)

    # Faixa de preço
    if filter.min_price is not None:
        query = query.filter(Property.price >= filter.min_price)

    if filter.max_price is not None:
        query = query.filter(Property.price <= filter.max_price)

    # Paginação
    query = query.offset(filter.offset).limit(filter.limit)

    properties = session.scalars(query).all()
    return {'properties': properties}


@router.put('/{property_id}', response_model=PropertyPublic)
def update_property(
    property_id: int,
    property: PropertySchema,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_property = session.scalar(
        select(Property).where(Property.id == property_id)
    )

    if not db_property:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Property not found'
        )

    for key, value in property.model_dump().items():
        if getattr(db_property, key) != value:
            setattr(db_property, key, value)

    session.commit()
    session.refresh(db_property)

    return db_property


@router.delete('/{property_id}', response_model=Message)
def delete_property(
    property_id: int,
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_property = session.scalar(
        select(Property).where(Property.id == property_id)
    )

    if not db_property:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Property not found'
        )

    session.delete(db_property)
    session.commit()

    return {'message': 'Property deleted'}
