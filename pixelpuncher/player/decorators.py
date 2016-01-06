from functools import wraps

from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect

from pixelpuncher.player.models import Player


def player_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        player = get_object_or_None(Player, user=user)

        if player is None:
            return redirect(reverse("player:new"))
        
        return func(request, player, *args, **kwargs)

    return wrapper
