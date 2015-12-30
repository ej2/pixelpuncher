from functools import wraps
from django.shortcuts import get_object_or_404

from pixelpuncher.player.models import Player


def player_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        player = get_object_or_404(Player, user=user)

        return func(request, player, *args, **kwargs)

    return wrapper
