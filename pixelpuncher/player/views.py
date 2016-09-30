from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from pixelpuncher.game.utils.combat import perform_skill_in_combat, perform_skill
from pixelpuncher.game.utils.message import add_game_message, get_game_messages
from pixelpuncher.item.utils import use_item, drop_item, examine_item
from pixelpuncher.player.decorators import player_required
from pixelpuncher.player.forms import PlayerForm, AttributeForm
from pixelpuncher.player.models import Player, Avatar, Achievement, PlayerSkill
from pixelpuncher.player.utils.avatar import get_unlocked_layers_by_type, set_avatar
from pixelpuncher.player.utils.collections import assign_player_collections


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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PlayerDetailView, self).dispatch(request, *args, **kwargs)

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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AttributeSpendView, self).dispatch(request, *args, **kwargs)

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


@login_required
@player_required
def drop(request, player, item_id):
    result = drop_item(item_id)
    add_game_message(player, result)

    return redirect(reverse("player:detail", args=[player.id]))


@login_required
@player_required
def use(request, player, item_id):
    result = use_item(player, item_id)
    add_game_message(player, result)

    return redirect(reverse("player:detail", args=[player.id]))


@login_required
@player_required
def examine(request, player, item_id):
    result = examine_item(item_id)
    add_game_message(player, result)

    return redirect(reverse("player:detail", args=[player.id]))


def top_punchers(request):
    if request.user.is_authenticated():
        player = get_object_or_None(Player, user=request.user)

        #assign_player_collections(player)  # Temp - needs to be added to login or nightly script
    else:
        player = None

    players = Player.objects.all().order_by("-xp")

    context = {
        "players": players,
        "player": player,
    }

    return TemplateResponse(
        request, "player/top_punchers.html", RequestContext(request, context))


@login_required
@player_required
def avatar_list(request, player):
    body_layers = get_unlocked_layers_by_type(player, 'body')
    hair_layers = get_unlocked_layers_by_type(player, 'hair')
    face_layers = get_unlocked_layers_by_type(player, 'face')
    shirt_layers = get_unlocked_layers_by_type(player, 'shirt')

    if request.method == "POST":
        body_id = request.POST["body_id"]
        hair_id = request.POST["hair_id"]
        face_id = request.POST["face_id"]
        shirt_id = request.POST["shirt_id"]

        set_avatar(player, hair_id, face_id, body_id, shirt_id)

        return redirect(reverse("player:detail", args=[player.id]))

    context = {
        "user": player.user,
        "player": player,
        "body_layers": body_layers,
        "hair_layers": hair_layers,
        "face_layers": face_layers,
        "shirt_layers": shirt_layers,

    }
    return TemplateResponse(
        request, "player/avatar_choose.html", RequestContext(request, context))


@login_required
@player_required
def choose_avatar(request, player, avatar_id):
    avatar = get_object_or_404(Avatar, pk=avatar_id)

    player.avatar = avatar
    player.save()

    return redirect(reverse("player:detail", args=[player.id]))


@login_required
@player_required
def view_achievements(request, player):
    context = {
        "user": player.user,
        "player": player,
    }

    return TemplateResponse(
        request, "player/achievements.html", RequestContext(request, context))


@login_required
@player_required
def skill(request, player, player_skill_id):
    player_skill = get_object_or_404(PlayerSkill, id=player_skill_id)
    perform_skill(player, player_skill)

    return redirect(reverse("player:detail", args=[player.id]))
