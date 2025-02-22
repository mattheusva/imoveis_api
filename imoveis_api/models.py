from sqlalchemy import Column, DateTime, Float, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, nullable=True)
    CRECI = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Property(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    area = Column(Float)
    rooms = Column(Integer)
    bathrooms = Column(Integer)
    garages = Column(Integer)
    price = Column(Float)
    transaction = Column(String)
    description = Column(String)
    address = Column(String)
    city = Column(String)
    state = Column(String)
    status = Column(String)
    created_at = Column(DateTime, server_default=func.now())
