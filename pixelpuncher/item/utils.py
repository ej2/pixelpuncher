import random

from annoying.functions import get_object_or_None
from django.db import transaction

from pixelpuncher.item.models import Item, LevelEquipment, PlayerContainer
from pixelpuncher.player.utils.avatar import unlock_layer


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
    item = None

    if item_type.stackable:
        item = get_object_or_None(Item, player=player, item_type=item_type)

    if item:
        item.remaining_uses += 1
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


def examine_item(item_id):
    item = get_object_or_None(Item, id=item_id)
    return item.item_type.description


def use_item(player, item_id):
    item = get_object_or_None(Item, id=item_id)

    if item:
        if item.item_type.base_type == "CON":
            result = use_consumable(player, item)

        elif item.item_type.base_type == "ARM":
            result = use_armor(player, item)

        elif item.item_type.base_type == "UNL":
            result = "Nothing happens..."

        elif item.item_type.base_type == "WEA":
            result = "Nothing happens..."

        else:
            result = "Nothing happens..."

    return result


def use_consumable(player, item):
    result = "You {0} the {1}. ".format(item.item_type.action_verb, item.item_type.name)

    if item.item_type.current_energy_bonus != 0:
        result += player.adjust_energy(item.item_type.current_energy_bonus)

    if item.item_type.current_health_bonus != 0:
        result += player.adjust_health(item.item_type.current_health_bonus)

    player.save()

    if item.item_type.stackable:
        item.remaining_uses -= 1

        if item.remaining_uses <= 0:
            item.delete()
        else:
            item.save()
    else:
        item.delete()

    return result


def use_armor(player, item):
    if item.item_type.classification == "HEAD":
        player.head = item
        result = "You put the {0} on your head.".format(item.item_type.name)
    elif item.item_type.classification == "GLOVE":
        player.gloves = item
        result = "You put the {0} on your hands.".format(item.item_type.name)
    elif item.item_type.classification == "TORSO":
        player.torso = item
        result = "You put the {0} on your torso.".format(item.item_type.name)
    else:
        result = "You cannot wear that."

    player.save()
    return result


def give_level_equipment(player):

    level_equipment = LevelEquipment.objects.filter(level=player.level)

    for equip in level_equipment:
        item = create_item(equip.item_type)
        item.player = player
        item.save()


def auto_equip(player):
    for item in player.items.all():
        if item.item_type.base_type == "ARM":
            use_armor(item)


def get_combat_items(player):
    return player.items.filter(item_type__combat_usable=True).order_by("item_type__name")


def sell_item(player, item, amount):
    if item.item_type.sellable:
        player.pixels += amount
        player.save()

        if item.item_type.stackable:
            item.remaining_uses -= 1

            if item.remaining_uses <= 0:
                item.delete()
            else:
                item.save()
        else:
            item.delete()

        return "You sell the {} for {} pixels.".format(item.item_type.name, amount)


def purchase_item(player, item_type, price, currency):
    if currency == 'P':
        currency_name = "Pixels"
        if player.pixels < price:
            return "You don't have enough to purchase that."

        with transaction.atomic():
            player.pixels -= price
            player.save()

    else:
        currency_name = "MegaPixels"
        if player.megapixels < price:
            return "You don't have enough to purchase that."

        with transaction.atomic():
            player.megapixels -= price
            player.save()

    add_item_type_to_player(item_type, player)
    if item_type.layer:
        unlock_layer(player, item_type.layer)

    return "You purchase the {} for {} {}.".format(item_type.name, price, currency_name)


def take_item_from_container(player, item):
    container_name = item.container.container.name

    if item.item_type.stackable:
        player_item = get_object_or_None(Item, player=player, item_type=item.item_type)

        if player_item is None:
            player_item = create_item(item.item_type)
            player_item.player = player
        else:
            player_item.remaining_uses += 1

        player_item.save()
        item.remaining_uses -= 1
        item.save()

        if item.remaining_uses == 0:
            item.delete()

        return "You take a {} from the {}.".format(item, container_name)
    else:
        item.player = player
        item.container = None
        item.save()

        return "You take the {} from the {}.".format(item, container_name)


def put_item_in_container(item, player_container):

    if item.item_type.stackable and item.remaining_uses > 1:

        container_item = get_object_or_None(Item, container=player_container, item_type=item.item_type)

        if container_item is None:
            container_item = create_item(item.item_type)
            container_item.container = player_container
        else:
            container_item.remaining_uses += 1

        container_item.save()
        item.remaining_uses -= 1
        item.save()

        return "You put a {} in the {}.".format(item, player_container.container.name)

    else:
        item.player = None
        item.container = player_container
        item.save()

        return "You put the {} in the {}.".format(item, player_container.container.name)


def assign_container(player, container):
    player_container = PlayerContainer()
    player_container.player = player
    player_container.container = container
    player_container.save()

    return player_container
