from http import HTTPStatus

from imoveis_api.schemas import PropertyPublic


def test_create_property(client):
    response = client.post(
        '/properties',
        json={
            'type': 'Apartamento',
            'area': 120.0,
            'rooms': 3,
            'bathrooms': 2,
            'garages': 1,
            'value': 500000.0,
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
        'value': 500000.0,
        'transaction': 'compra',
        'description': 'Ótima localização.',
        'address': 'Rua Exemplo, 123',
        'city': 'São Paulo',
        'state': 'SP',
        'status': 'Disponível',
    }


def test_read_properties(client):
    response = client.get('/properties')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'properties': []}


def test_read_properties_with_property(client, property):
    property_schema = PropertyPublic.model_validate(property).model_dump()
    response = client.get('/properties/')
    assert response.json() == {'properties': [property_schema]}


def test_update_property(client, property):
    response = client.put(
        '/properties/1',
        json={
            'type': 'Casa',
            'area': 80.0,
            'rooms': 2,
            'bathrooms': 1,
            'garages': 2,
            'value': 450000.0,
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
        'value': 450000.0,
        'transaction': 'aluguel',
        'description': 'Boa localização.',
        'address': 'Rua Teste, 123',
        'city': 'Porto Alegre',
        'state': 'RS',
        'status': 'Indisponivel',
    }


def test_delete_property(client, property):
    response = client.delete('/properties/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Property deleted'}
