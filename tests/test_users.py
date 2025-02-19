from http import HTTPStatus

from imoveis_api.schemas import UserPublic
from imoveis_api.security import create_access_token


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'matheus',
            'email': 'matheus@email.com',
            'password': '123456',
            'phone': '+55 51 99999-9999',
            'CRECI': '999999',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'matheus',
        'email': 'matheus@email.com',
        'phone': '+5551999999999',
        'CRECI': '999999',
        'id': 1,
    }


def test_create_user_without_phone_and_creci(client):
    response = client.post(
        '/users',
        json={
            'username': 'matheus',
            'email': 'matheus@email.com',
            'password': '123456',
            'phone': None,
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'matheus',
        'email': 'matheus@email.com',
        'phone': None,
        'CRECI': None,
        'id': 1,
    }


def test_create_user_with_invalid_phone_format(client):
    response = client.post(
        '/users',
        json={
            'username': 'matheus',
            'email': 'matheus@email.com',
            'password': '123456',
            'phone': '+55 51 99999-99999',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response_data = response.json()
    detail = response_data['detail']
    msg = detail[0]['msg']
    assert msg == 'Value error, Invalid phone number'


def test_create_user_with_invalid_phone(client):
    response = client.post(
        '/users',
        json={
            'username': 'matheus',
            'email': 'matheus@email.com',
            'password': '123456',
            'phone': '12345',
        },
    )
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    response_data = response.json()
    detail = response_data['detail']
    msg = detail[0]['msg']
    assert msg == 'Value error, Invalid phone number'


def test_create_user_should_return_400_username_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': user.username,
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_should_return_400_email_exists(client, user):
    response = client.post(
        '/users',
        json={
            'username': 'Alice',
            'email': user.email,
            'password': 'testtest',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
            'phone': '+5511912345678',
            'CRECI': '666666',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'phone': '+5511912345678',
        'CRECI': '666666',
        'id': user.id,
    }


def test_update_integrity_error(client, user, token):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )
    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_get_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
