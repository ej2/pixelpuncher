import random

from django.db.models import Q
from pixelpuncher.player.models import AvatarLayer, PlayerAvatar
from annoying.functions import get_object_or_None


def get_unlocked_layers_by_type(player, layer_type):
    ids = player.layers.filter(layer__layer_type=layer_type).values_list('layer__id', flat=True)
    layers = AvatarLayer.objects.filter(Q(layer_type=layer_type) & (Q(unlock_method='start') | Q(id__in=ids)))

    return layers


def set_avatar(player, hair_id, face_id, body_id, shirt_id):

    for layer in player.layers.all():
        layer.current = False
        layer.save()

    hair_layer, created = PlayerAvatar.objects.get_or_create(player=player, layer_id=hair_id)
    hair_layer.current = True
    hair_layer.save()

    face_layer, created = PlayerAvatar.objects.get_or_create(player=player, layer_id=face_id)
    face_layer.current = True
    face_layer.save()

    body_layer, created = PlayerAvatar.objects.get_or_create(player=player, layer_id=body_id)
    body_layer.current = True
    body_layer.save()

    shirt_layer, created = PlayerAvatar.objects.get_or_create(player=player, layer_id=shirt_id)
    shirt_layer.current = True
    shirt_layer.save()


def generate_random_starting_avatar(player):
    body_layer = random.choice(get_unlocked_layers_by_type(player, 'body'))
    hair_layer = random.choice(get_unlocked_layers_by_type(player, 'hair'))
    face_layer = random.choice(get_unlocked_layers_by_type(player, 'face'))
    shirt_layer = random.choice(get_unlocked_layers_by_type(player, 'shirt'))

    set_avatar(player, body_layer.id, hair_layer.id, face_layer.id, shirt_layer.id)


def unlock_layer(player, layer):
    """
    Unlocks a avatar layer for a player
    :param player:
    :param layer:
    :return: True if layer was unlocked
    """
    player_avatar = get_object_or_None(PlayerAvatar, player=player, layer=layer)

    if player_avatar is None:
        player_avatar = PlayerAvatar(player=player, layer=layer)
        player_avatar.save()

        return True
    else:
        return False
