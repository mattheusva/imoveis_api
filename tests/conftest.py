import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from testcontainers.postgres import PostgresContainer

from imoveis_api.app import app
from imoveis_api.database import get_session
from imoveis_api.models import Base
from imoveis_api.security import get_password_hash
from tests.factories import PropertyFactory, UserFactory


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_async_engine(postgres.get_connection_url())
        yield _engine


@pytest_asyncio.fixture
async def session(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def user(session):
    pwd = 'testtest'

    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest_asyncio.fixture
async def other_user(session):
    user = UserFactory()

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@pytest_asyncio.fixture
async def property(session):
    property = PropertyFactory()
    session.add(property)
    await session.commit()
    await session.refresh(property)

    return property


@pytest.fixture
def token(client, user):
    response = client.post(
        'auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
