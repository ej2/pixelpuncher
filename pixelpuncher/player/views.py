from annoying.functions import get_object_or_None
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, DetailView, UpdateView

from pixelpuncher.game.utils.message import add_game_message, get_game_messages
from pixelpuncher.item.utils import use_item, drop_item
from pixelpuncher.player.decorators import player_required
from pixelpuncher.player.forms import PlayerForm, AttributeForm
from pixelpuncher.player.models import Player


class PlayerCreateView(CreateView):
    model = Player
    template_name = "player/create.html"
    form_class = PlayerForm

    def get_form_kwargs(self):
        kwargs = super(PlayerCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save()

        return redirect(reverse("player:detail", args=[self.object.pk]))


class PlayerDetailView(DetailView):
    model = Player
    template_name = "player/detail.html"
    context_object_name = "player"
    pk_url_kwarg = "player_id"

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        context['game_messages'] = get_game_messages(self.object)
        return context


class AttributeSpendView(UpdateView):
    model = Player
    form_class = AttributeForm
    template_name = "player/attribute.html"
    context_object_name = "player"
    pk_url_kwarg = "player_id"

    def form_valid(self, form):
        self.object = form.save()

        return redirect(reverse("player:detail", args=[self.object.pk]))


def player_redirect(request):
    user = request.user
    player = get_object_or_None(Player, user=user)

    if player:
        return redirect(reverse("player:detail", args=[player.id]))
    else:
        return redirect(reverse("player:new"))


@player_required
def drop(request, player, item_id):
    result = drop_item(item_id)
    add_game_message(player, result)

    return redirect(reverse("player:detail", args=[player.id]))


@player_required
def use(request, player, item_id):
    result = use_item(item_id)
    add_game_message(player, result)

    return redirect(reverse("player:detail", args=[player.id]))

