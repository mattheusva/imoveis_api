import factory

from imoveis_api.models import Property, User
from imoveis_api.schemas import TransactionType


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
