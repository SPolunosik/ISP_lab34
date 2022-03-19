from ugc.models import Item, Profiler, ShoppingBasket

def get_all_user():
    return Profiler.objects.all()


def get_or_create_user(*args, **kwargs):
    return Profiler.objects.get_or_create(*args, **kwargs)[0]


def get_all_items():
    return Item.objects.all()


def get_item(*args, **kwargs):
    return Item.objects.get(*args, **kwargs)

def filter_items(*args, **kwargs):
    return Item.objects.filter(*args, **kwargs)


def create_item(*args, **kwargs):
    return Item(*args, **kwargs)


def update_item(callbackcontextargs, *args, **kwargs):
    item = get_item(*args, **kwargs)
    for param in callbackcontextargs:
        pair = param.split(sep='=')
        setattr(item, pair[0], pair[1])
    item.save()


def delete_item(*args, **kwargs):
    return get_item(*args, **kwargs).delete()


def get_or_create_cart(*args, **kwargs):
    return ShoppingBasket.objects.get_or_create(*args, **kwargs)[0]


def delete_item_from_cart(cart, *args, **kwargs):
    cart.items.remove(cart.items.get(*args, **kwargs))
