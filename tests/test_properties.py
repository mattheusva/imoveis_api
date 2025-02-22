from http import HTTPStatus

from imoveis_api.schemas import PropertyPublic


def test_create_property(client, token):
    response = client.post(
        '/properties',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'type': 'Apartamento',
            'area': 120.0,
            'rooms': 3,
            'bathrooms': 2,
            'garages': 1,
            'price': 500000.0,
            'transaction': 'compra',
            'description': 'Ótima localização.',
            'address': 'Rua Exemplo, 123',
            'city': 'São Paulo',
            'state': 'SP',
            'status': 'Disponível',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'type': 'Apartamento',
        'area': 120.0,
        'rooms': 3,
        'bathrooms': 2,
        'garages': 1,
        'price': 500000.0,
        'transaction': 'compra',
        'description': 'Ótima localização.',
        'address': 'Rua Exemplo, 123',
        'city': 'São Paulo',
        'state': 'SP',
        'status': 'Disponível',
    }


def test_list_properties(client):
    response = client.get('/properties')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'properties': []}


def test_list_properties_with_property(client, property):
    property_schema = PropertyPublic.model_validate(property).model_dump()
    response = client.get('/properties/')
    assert response.json() == {'properties': [property_schema]}


def test_update_property(client, property, token):
    response = client.put(
        f'/properties/{property.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'type': 'Casa',
            'area': 80.0,
            'rooms': 2,
            'bathrooms': 1,
            'garages': 2,
            'price': 450000.0,
            'transaction': 'aluguel',
            'description': 'Boa localização.',
            'address': 'Rua Teste, 123',
            'city': 'Porto Alegre',
            'state': 'RS',
            'status': 'Indisponivel',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'type': 'Casa',
        'area': 80.0,
        'rooms': 2,
        'bathrooms': 1,
        'garages': 2,
        'price': 450000.0,
        'transaction': 'aluguel',
        'description': 'Boa localização.',
        'address': 'Rua Teste, 123',
        'city': 'Porto Alegre',
        'state': 'RS',
        'status': 'Indisponivel',
    }


def test_update_property_should_return_not_found(client, token):
    response = client.put(
        '/properties/666',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'type': 'Casa',
            'area': 80.0,
            'rooms': 2,
            'bathrooms': 1,
            'garages': 2,
            'price': 450000.0,
            'transaction': 'aluguel',
            'description': 'Boa localização.',
            'address': 'Rua Teste, 123',
            'city': 'Porto Alegre',
            'state': 'RS',
            'status': 'Indisponivel',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Property not found'}


def test_delete_property(client, property, token):
    response = client.delete(
        f'/properties/{property.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Property deleted'}


def test_delete_property_should_return_not_found(client, token):
    response = client.delete(
        '/properties/666',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Property not found'}
