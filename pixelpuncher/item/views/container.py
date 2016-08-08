from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.item.forms import ContainerForm
from pixelpuncher.item.models import PlayerContainer, Item
from pixelpuncher.item.utils import take_item_from_container, drop_item
from pixelpuncher.player.decorators import player_required


@login_required
@player_required
def open_container(request, player, container_id):
    request.session['container_id'] = container_id
    player_container = get_object_or_404(PlayerContainer, id=container_id)

    if request.method == "POST":
        form = ContainerForm(request.POST, player_container=player_container)
        result = form.save()
        add_game_message(player, result)
    else:
        form = ContainerForm(player_container=player_container)

    context = {
        "user": player.user,
        "player": player,
        "player_container": player_container,
        "form": form
    }

    return TemplateResponse(
        request, "item/container/detail.html", RequestContext(request, context))


@login_required
@player_required
def take_item(request, player, item_id):
    item = get_object_or_404(Item, pk=item_id)
    player_container_id = item.container.pk

    if item.container.player == player:
        result = take_item_from_container(player, item)
        add_game_message(player, result)

    return redirect("container:open", player_container_id)


@login_required
@player_required
def discard_item(request, player, item_id):
    item = get_object_or_404(Item, pk=item_id)
    player_container_id = item.container.pk

    if item.container.player == player:
        result = drop_item(item.pk)
        add_game_message(player, result)

    return redirect("container:open", player_container_id)
