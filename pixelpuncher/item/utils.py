import random
from annoying.functions import get_object_or_None

from pixelpuncher.item.models import Item


def create_item(item_type):
    item = Item.objects.create(
        item_type=item_type,
        remaining_uses=item_type.total_uses,
    )

    return item


def get_random_drop(drop_table):
    drop = random.randint(1, drop_table.max_rate)

    item_drops = drop_table.items.filter(drop_rate__gt=drop)

    if item_drops.count() > 0:
        item_drop = random.choice(item_drops)
        return item_drop.item_type
    else:
        return None


def add_item_type_to_player(item_type, player):

    if item_type.stackable:
        item = get_object_or_None(Item, player=player, item_type=item_type)

        if item:
            item.remaining_uses += 1
            item.save()
        else:
            item = create_item(item_type)
            item.player = player
            item.save()

    else:
        item = create_item(item_type)
        item.player = player
        item.save()

    return item


def drop_item(item_id):
    item = get_object_or_None(Item, id=item_id)
    result = "You drop the {0}. ".format(item.item_type.name)
    item.delete()

    return result


def use_item(item_id):
    item = get_object_or_None(Item, id=item_id)

    if item:
        if item.item_type.base_type == "CON":
            result = use_consumable(item)

        elif item.item_type.base_type == "ARM":
            result = use_armor(item)
        elif item.item_type.base_type == "WEA":
            pass

    return result


def use_consumable(item):
    result = "You {0} the {1}. ".format(item.item_type.action_verb, item.item_type.name)

    if item.item_type.current_energy_bonus != 0:
        result += item.player.adjust_energy(item.item_type.current_energy_bonus)

    if item.item_type.current_health_bonus != 0:
        result += item.player.adjust_health(item.item_type.current_health_bonus)

    item.player.save()

    if item.item_type.stackable:
        item.remaining_uses -= 1

        if item.remaining_uses <= 0:
            item.delete()
        else:
            item.save()
    else:
        item.delete()

    return result


def use_armor(item):

    if item.item_type.classification == "HEAD":
        item.player.head = item
        item.player.save()
        result = "You put the {0} on your head.".format(item.item_type.name)
    elif item.item_type.classification == "GLOVE":
        item.player.gloves = item
        item.player.save()
        result = "You put the {0} on your hands.".format(item.item_type.name)
    else:
        result = "You cannot wear that."

    return result
