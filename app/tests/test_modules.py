from ugc.management.commands.handler import create_item
import pytest
import uuid
from ugc.controller import get_or_create_cart, get_or_create_user



@pytest.fixture
def user_data():
    return {"external_id": 646366, "name": "sergei1234567890"}

id_test=uuid.uuid4()

@pytest.fixture
def item_data():
    return {"id": id_test, "cost": 50, "name": "Iphone"}


@pytest.fixture
def user_bd():
    return get_or_create_user(external_id=646366, name="sergei1234567890")


@pytest.fixture
def item_bd(user_bd):
    return create_item(profiler=user_bd, id=id_test, name="Iphone", cost=50)


def check(d: dict, item):
    for key, value in d.items():
        assert getattr(item, key) == value


@pytest.mark.django_db
def test_user_type(user_data, user_bd):
    check(user_data, user_bd)


@pytest.mark.django_db
def test_item_type(item_data, item_bd):
    check(item_data, item_bd)


class MyCallBack:
    args = []

    def __init__(self, s):
        def try_int(item):
            try:
                return int(item)
            except ValueError:
                return item

        self.args = list(map(try_int, s.split()))


test_data = [("name=Iphone cost=50", "Iphone", 50), ("cost=100 name=TV", "TV", 100), ("cost=6 name=flower", "flower", 6)]

@pytest.mark.django_db
@pytest.mark.parametrize("args, name, cost", test_data)
def test_shopping_basket(args, name, cost, user_bd):
    shops =  get_or_create_cart(profiler=user_bd)

    item, id = create_item(user_bd, MyCallBack(args))

    shops.items.add(item)

    assert shops.items.get(profiler=user_bd,name=name) == item

    assert len(shops.items.all()) == 1

    shops.items.remove(item)

    assert len(shops.items.all()) == 0
