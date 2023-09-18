import factory

from htmx_demo.core.models import Product
from htmx_demo.utils.factories import BaseMetaFactory


class ProductFactory(
    factory.django.DjangoModelFactory,
    metaclass=BaseMetaFactory[Product],
):
    name = factory.Faker("company")
    description = factory.Faker("paragraph")
    price_cents = factory.Faker("pyint")

    class Meta:
        model = Product
