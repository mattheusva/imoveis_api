from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from imoveis_api.database import get_session
from imoveis_api.models import Property
from imoveis_api.schemas import Message, PropertySchema, PropertyPublic, PropertyList

router = APIRouter(prefix='/properties', tags=['properties'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=PropertyPublic)
def create_property(property: PropertySchema, session: Session = Depends(get_session)):
    new_property = Property(**property.model_dump())
    session.add(new_property)
    session.commit()
    session.refresh(new_property)

    return new_property


@router.get('/', response_model=PropertyList)
def read_properties(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    properties = session.scalars(select(Property).offset(skip).limit(limit)).all()
    return {'properties': properties}


@router.put('/{property_id}', response_model=PropertyPublic)
def update_property(
    property_id: int, property: PropertySchema, session: Session = Depends(get_session)
):
    db_property = session.scalar(select(Property).where(Property.id == property_id))

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
def delete_property(property_id: int, session: Session = Depends(get_session)):
    db_property = session.scalar(select(Property).where(Property.id == property_id))

    if not db_property:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Property not found'
        )
    
    session.delete(db_property)
    session.commit()

    return {'message': 'Property deleted'}
