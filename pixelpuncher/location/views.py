from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.item.models import Item
from pixelpuncher.item.utils import purchase_item, sell_item
from pixelpuncher.location.models import Location, LocationItem, LocationService
from pixelpuncher.location.utils import purchase_service, perform_service
from pixelpuncher.npc.utils.conversation import get_merchant_greeting
from pixelpuncher.npc.utils.relationships import get_relationship
from pixelpuncher.player.decorators import player_required


@login_required
@player_required
def visit_location(request, player, location_id):
    request.session['location_id'] = location_id
    location = get_object_or_404(Location, id=location_id)

    if location.npc:
        relationship = get_relationship(player, location.npc)
    else:
        relationship = None

    if location.location_type == 'ADV':
        return redirect("game:play")  # Temporary...

    if location.npc and location.location_type == 'SHP':
        add_game_message(player, get_merchant_greeting(location))

    context = {
        "user": player.user,
        "player": player,
        "relationship": relationship,
        "location": location,
    }

    return TemplateResponse(
        request, "location/visit.html", RequestContext(request, context))


@login_required
@player_required
def visit_home(request, player):
    location = player.locations.filter(location_type='HOM')[0]

    if location.npc:
        relationship = get_relationship(player, location.npc)
    else:
        relationship = None

    if location.location_type == 'ADV':
        return redirect("game:play")  # Temporary...

    if location.npc and location.location_type == 'SHP':
        add_game_message(player, get_merchant_greeting(location))

    context = {
        "user": player.user,
        "player": player,
        "location": location,
        "relationship": relationship,
    }

    return TemplateResponse(
        request, "location/visit.html", RequestContext(request, context))


@login_required
@player_required
def purchase(request, player, location_id, locationitem_id):
    location_item = get_object_or_404(LocationItem, pk=locationitem_id)

    result = purchase_item(player, location_item.item_type, location_item.price, location_item.currency)
    add_game_message(player, result)

    return redirect("location:visit", location_id)


@login_required
@player_required
def sell(request, player, location_id, item_id):
    item = get_object_or_404(Item, pk=item_id)
    amount = item.item_type.sell_price

    result = sell_item(player, item, amount)
    add_game_message(player, result)

    return redirect("location:visit", location_id)


@login_required
@player_required
def service(request, player, location_id, locationservice_id):
    location_service = get_object_or_404(LocationService, pk=locationservice_id)

    purchase_service(player, location_service)

    if location_service.service.page:
        return redirect(location_service.service.page, locationservice_id)
    else:
        result = perform_service(player, location_service.service)
        add_game_message(player, result)
        return redirect("location:visit", location_id)

