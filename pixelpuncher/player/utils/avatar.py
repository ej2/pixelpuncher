from django.db.models import Q
from pixelpuncher.player.models import AvatarLayer, PlayerAvatar


def get_unlocked_layers_by_type(player, layer_type):
    ids = player.layers.filter(layer__layer_type=layer_type).values_list('id', flat=True)
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
