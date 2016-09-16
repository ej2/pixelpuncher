from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import item_dropped, item_added_to_collection
from pixelpuncher.item.utils import add_item_type_to_player
from pixelpuncher.player.models import PlayerCollection, Collection


def give_collection_reward(player_collection):
    if player_collection.completed:
        player_collection.player.xp = player_collection.collection.reward_xp
        player_collection.player.save()

        item = add_item_type_to_player(player_collection.collection.reward_item, player_collection.player)
        add_game_message(player_collection.player, item_dropped(item))

        player_collection.reward_given = True
        player_collection.save()

        if player_collection.collection.achievement:
            player_collection.collection.achievement.players.add(player_collection.player)


def start_collection(player, collection):
    player_collection = PlayerCollection()
    player_collection.player = player
    player_collection.collection = collection
    player_collection.save()

    return player_collection


def item_type_in_collection(item_type, collection):
    if item_type in collection.items.all():
        return True
    else:
        return False


def item_unlocked(item_type, player_collection):
    if item_type in player_collection.found_items.all():
        return True
    else:
        return False


def add_item_to_collection(item_type, player_collection):
    player_collection.found_items.add(item_type)


def check_collections(player, item_type):
    for player_collection in player.collections.all():
        if item_type_in_collection(item_type, player_collection.collection):
            if not item_unlocked(item_type, player_collection):
                add_item_to_collection(item_type, player_collection)
                add_game_message(player, item_added_to_collection(item_type, player_collection.collection))

        if player_collection.is_complete:
            give_collection_reward(player_collection)


def create_player_collection(player, collection):
    player_collection = PlayerCollection()
    player_collection.player = player
    player_collection.collection = collection
    player_collection.save()

    return player_collection


def assign_player_collections(player):
    collections = Collection.objects.filter(active=True)

    for collection in collections:
        create_player_collection(player, collection)
