from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá, mundo!'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'matheus',
            'email': 'matheus@email.com',
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'matheus',
        'email': 'matheus@email.com',
    }
