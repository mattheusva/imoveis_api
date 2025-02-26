from http import HTTPStatus

import factory
import pytest

from tests.conftest import PropertyFactory


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


@pytest.mark.asyncio
async def test_list_properties_should_return_5(client, session):
    expected_properties = 5
    session.add_all(PropertyFactory.create_batch(5))
    await session.commit()

    response = client.get('/properties')
    assert len(response.json()['properties']) == expected_properties


@pytest.mark.asyncio
async def test_list_properties_pagination_should_return_2(
    client,
    session,
):
    expected_properties = 2
    session.add_all(PropertyFactory.create_batch(5))
    await session.commit()

    response = client.get('/properties/?offset=1&limit=2')
    assert len(response.json()['properties']) == expected_properties


@pytest.mark.asyncio
async def test_list_properties_filter_state_should_return_5(client, session):
    expected_properties = 5
    session.add_all(PropertyFactory.create_batch(5, state='SP'))
    await session.commit()

    response = client.get(
        '/properties/?state=SP',
    )
    assert len(response.json()['properties']) == expected_properties


@pytest.mark.asyncio
async def test_list_properties_filter_city_should_return_5(client, session):
    expected_properties = 5
    session.add_all(PropertyFactory.create_batch(5, city='São Paulo'))
    await session.commit()

    response = client.get(
        '/properties/?city=São Paulo',
    )
    assert len(response.json()['properties']) == expected_properties


@pytest.mark.asyncio
async def test_list_properties_filter_transaction_should_return_5(
    client, session
):
    expected_properties = 5
    session.add_all(PropertyFactory.create_batch(5, transaction='venda'))
    await session.commit()

    response = client.get(
        '/properties/?transaction=venda',
    )
    assert len(response.json()['properties']) == expected_properties


@pytest.mark.asyncio
async def test_list_properties_filter_type_should_return_5(client, session):
    expected_properties = 5
    session.add_all(PropertyFactory.create_batch(5, type='apartamento'))
    await session.commit()

    response = client.get(
        '/properties/?type=apartamento',
    )
    assert len(response.json()['properties']) == expected_properties


@pytest.mark.asyncio
async def test_list_properties_filter_min_max_price_range_should_return_5(
    client, session
):
    expected_properties = 5
    # Cria 5 propriedades dentro da faixa de preço
    in_range_prices = [300000.0, 350000.0, 400000.0, 450000.0, 500000.0]
    session.add_all(
        PropertyFactory.create_batch(
            5, price=factory.Iterator(in_range_prices)
        )
    )
    # Cria propriedades fora da faixa para testar o filtro
    session.add_all(PropertyFactory.create_batch(3, price=250000.0))
    session.add_all(PropertyFactory.create_batch(2, price=550000.0))
    await session.commit()

    response = client.get('/properties/?min_price=300000&max_price=500000')
    assert len(response.json()['properties']) == expected_properties


@pytest.mark.asyncio
async def test_list_properties_filter_combined(client, session):
    expected_properties = 5
    session.add_all(
        PropertyFactory.create_batch(
            5,
            state='RS',
            city='Imbé',
            transaction='aluguel',
            type='apartamento',
        )
    )
    await session.commit()

    response = client.get(
        '/properties/?state=RS&city=Imbé&transaction=aluguel&type=apartamento',
    )
    assert len(response.json()['properties']) == expected_properties


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
