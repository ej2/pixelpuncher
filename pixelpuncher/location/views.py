from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.item.utils import purchase_item
from pixelpuncher.location.models import Location, LocationItem
from pixelpuncher.npc.utils.conversation import get_merchant_greeting
from pixelpuncher.player.decorators import player_required


@login_required
@player_required
def visit_location(request, player, location_id):
    location = get_object_or_404(Location, id=location_id)

    add_game_message(player, get_merchant_greeting(location))
    context = {
        "user": player.user,
        "player": player,
        "location": location,
    }

    return TemplateResponse(
        request, "location/visit.html", RequestContext(request, context))


@login_required
@player_required
def purchase(request, player, location_id, locationitem_id):
    location_item = get_object_or_404(LocationItem, pk=locationitem_id)

    result = purchase_item(player, location_item.item_type, location_item.price)
    add_game_message(player, result)

    return redirect("location:visit", location_id)
