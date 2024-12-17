from http import HTTPStatus

from fastapi.testclient import TestClient

from imoveis_api.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_create_user():
    client = TestClient(app)

    response = client.post(
        '/users',
        json={
            'username': 'Matheus',
            'email': 'matheus@email.com',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Matheus',
        'email': 'matheus@email.com',
    }
