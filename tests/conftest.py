import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from imoveis_api.app import app
from imoveis_api.database import get_session
from imoveis_api.models import Base, Property, User
from imoveis_api.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'testtest'

    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(pwd),
        phone='55 51 99999-9999',
        CRECI='999999',
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd # Monkey Patch

    return user


@pytest.fixture
def property(session):
    property = Property(
        type='teste',
        area=120.0,
        rooms=4,
        bathrooms=2,
        garages=1,
        value=500000.0,
        transaction='aluguel',
        description='Boa localização',
        address='Rua teste',
        city='São Paulo',
        state='SP',
        status='Disponível',
    )
    session.add(property)
    session.commit()
    session.refresh(property)

    return property
