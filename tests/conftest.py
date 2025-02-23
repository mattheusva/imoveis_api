import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from imoveis_api.app import app
from imoveis_api.database import get_session
from imoveis_api.models import Base, Property, User
from imoveis_api.schemas import TransactionType
from imoveis_api.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    phone = '55 51 99999-9999'
    CRECI = '999999'


class PropertyFactory(factory.Factory):
    class Meta:
        model = Property

    type = factory.Faker(
        'random_element', elements=('casa', 'apartamento', 'terreno')
    )
    area = factory.Faker('pyfloat', min_value=50, max_value=1000)
    rooms = factory.Faker('random_int', min=1, max=6)
    bathrooms = factory.Faker('random_int', min=1, max=4)
    garages = factory.Faker('random_int', min=0, max=2)
    price = factory.Faker('pydecimal', left_digits=6, right_digits=2)
    transaction = factory.Faker(
        'random_element', elements=([t.value for t in TransactionType])
    )
    description = factory.Faker('paragraph')
    address = factory.Faker('street_address')
    city = factory.Faker('city')
    state = factory.Faker('state_abbr')
    status = factory.Faker(
        'random_element', elements=('Disponível', 'Reservado', 'Vendido')
    )


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

    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest.fixture
def other_user(session):
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def property(session):
    property = PropertyFactory()
    session.add(property)
    session.commit()
    session.refresh(property)

    return property


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
