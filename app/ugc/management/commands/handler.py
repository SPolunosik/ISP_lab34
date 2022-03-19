import uuid
from telegram.error import BadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
import multiprocessing
import requests
from . import TOKEN, PROXY_URL
from ugc.controller import delete_item, delete_item_from_cart, filter_items, get_all_items, get_all_user, get_or_create_cart, get_or_create_user, update_item, create_item
import logging

def send_to_all_user(message):
    procs = []
    for user in get_all_user():
        p = multiprocessing.Process(
            target=send_message, kwargs={"chat_id": user.external_id, "message": message})
        p.start()
        procs.append(p)

    for p in procs:
        p.join()


def send_message(chat_id, message):
    url = f"{PROXY_URL}{TOKEN}/sendMessage?chat_id={chat_id}&parser_mod=Markdown&text={message}"
    response = requests.get(url)
    return response.json()


def get_user(update):
    char_id = update.message.chat_id
    p= get_or_create_user(
        external_id=char_id,
        defaults={
            "name": update.message.from_user.username
        }
    )
    return p


def start_bot_callback(update, callbackcontext):
    p = get_user(update)
    update.message.reply_text("Hi, " + p.name + "!")


def show_item_callback(update, callbackcontext):
    items_info = []
    try:
        if len(callbackcontext.args) >= 1:
            for item in callbackcontext.args:
                items = filter_items(name=item)
                for res in items:
                    items_info.append(str(res))
        else:
            for item in get_all_items():
                items_info.append(str(item))
    except ObjectDoesNotExist:
        pass
    if len(items_info) != 0:
        for item in items_info:
            update.message.reply_text(item)
    else:
        update.message.reply_text("No items for you was found")


def create_and_fill_item(user, callbackcontext):
    logging.error(callbackcontext.args)
    test = uuid.uuid4()
    item = create_item(profiler=user, id=test)
    for param in callbackcontext.args:
        pair = param.split(sep='=')
        setattr(item, pair[0], pair[1])
    item.save()
    return item, test


def create_item_callback(update, callbackcontext):
    if len(callbackcontext.args) >= 1:
        p = get_user(update)
        try:
            item, id = create_and_fill_item(p, callbackcontext)
            update.message.reply_text("success, create id:")
            update.message.reply_text(str(id))
        except (AttributeError, ValueError, IndexError, IntegrityError, KeyError) as ex:
            update.message.reply_text("Write the correct data")
    else:
        update.message.reply_text(
            'Please, enter format item: [/create] [option]=[something] ...')


def update_item_callback(update, callbackcontext):
    if len(callbackcontext.args) >= 1:
        u = get_user(update)
        try:
            try:
                id = uuid.UUID(callbackcontext.args[0])
            except ValueError:
                raise ObjectDoesNotExist("")
            update_item(callbackcontext.args[1:], profiler=u, id=id)
            update.message.reply_text("success changed")
        except ObjectDoesNotExist:
            update.message.reply_text("ID not found")
        except ValueError as ex:
            update.message.reply_text("Write the correct data")
    else:
        update.message.reply_text(
            'Please, enter format item: [/update] id [option]=[something] ...')


def delete_item_callback(update, callbackcontext):
    if len(callbackcontext.args) == 1:
        u = get_user(update)
        try:
            id = uuid.UUID(callbackcontext.args[0])
            delete_item(profiler=u, id=id)
            update.message.reply_text("success deleted")
        except (ObjectDoesNotExist, ValueError):
            update.message.reply_text("ID not found")
    else:
        update.message.reply_text(
            'Please, enter format item: [/delete] id')


def pars_args(callbackcontext):
    pairs = {}
    for param in callbackcontext.args:
            pair = param.split(sep='=')
            pairs[pair[0]] = pair[1]
    pairs["profiler"] = get_or_create_user(name=pairs["user"])
    del pairs['user']
    return pairs


def buy_item_callback(update, callbackcontext):
    try:
        u = get_user(update)
        if len(callbackcontext.args) == 0:
            try:
                shops = get_or_create_cart(profiler=u)
                items_info = []
                for item in shops.items.all():
                    items_info.append(str(item))
                    items_info.append("\n")
                update.message.reply_text("\n".join(items_info))
            except (ObjectDoesNotExist, IndexError, ValueError, IntegrityError, KeyError) as ex:
                update.message.reply_text("No items in cart")
        elif callbackcontext.args[0] == "delete":
            try:
                callbackcontext.args = callbackcontext.args[1:]
                pairs = pars_args(callbackcontext)
                shop = get_or_create_cart(profiler=get_user(update))
                delete_item_from_cart(shop, **pairs)
            except (ObjectDoesNotExist, IndexError, ValueError, IntegrityError, KeyError) as ex:
                update.message.reply_text("Item not found")
            update.message.reply_text("success deleted")
        else:
            try:
                pairs = pars_args(callbackcontext)
                shop = get_or_create_cart(profiler=get_user(update))
                shop.save()
                item = filter_items(**pairs)[0]
                shop.items.add(item)
                update.message.reply_text("success added")
            except (ObjectDoesNotExist, IndexError, ValueError, IntegrityError, KeyError) as ex:
                update.message.reply_text("Item not found")
    except BadRequest as br:
        update.message.reply_text("No items in cart")


def unknown_command_callback(update, callbackcontext):
    update.message.reply_text(
        "Sorry, the command is not supported or not allowed.")
