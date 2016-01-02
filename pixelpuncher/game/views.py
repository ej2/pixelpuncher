from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.utils import game_settings
from pixelpuncher.game.utils.combat import perform_skip, perform_skill, perform_taunt
from pixelpuncher.game.utils.encounter import get_enemy
from pixelpuncher.game.utils.game import can_punch
from pixelpuncher.game.utils.leveling import xp_required_for_level
from pixelpuncher.game.utils.message import get_game_messages
from pixelpuncher.player.decorators import player_required
from pixelpuncher.player.models import PlayerSkill, VICTORY, COMBAT, PASSIVE


@player_required
def play(request, player):
    can_punch_flag = can_punch(player)

    enemy = None

    if can_punch_flag:
        if player.status == VICTORY:
            player.status = PASSIVE
            player.save()

        elif player.status == PASSIVE:
            if can_punch_flag:
                enemy = get_enemy(player)
                player.status = COMBAT
                player.save()

        elif player.status == COMBAT:
            enemy = get_enemy(player)

    game_messages = get_game_messages(player)

    context = {
        "user": player.user,
        "player": player,
        "enemy": enemy,
        "game_messages": game_messages,
        "can_punch": can_punch_flag,
    }

    return TemplateResponse(
        request, "game/play.html", RequestContext(request, context))


@player_required
def skill(request, player, player_skill_id):
    player_skill = get_object_or_404(PlayerSkill, id=player_skill_id)
    perform_skill(player, player_skill)

    return redirect(reverse("game:play"))


@player_required
def taunt(request, player):
    perform_taunt(player)
    return redirect(reverse("game:play"))


@player_required
def skip(request, player):
    perform_skip(player)
    return redirect(reverse("game:play"))


@player_required
def reset(request, player):
    player.punches = game_settings.DAILY_PUNCHES
    player.current_health = player.total_health
    player.current_energy = player.total_energy
    player.save()

    return redirect(reverse("game:play"))

@player_required
def level_requirements(request, player):
    levels = []
    previous = 0

    for x in range(1, 21):
        xp = int(xp_required_for_level(x))
        levels.append({
            "level": x,
            "xp": xp,
            "diff": xp - previous
        })

        previous = xp

    context = {
        "levels": levels,
        "player": player
    }

    return TemplateResponse(
        request, "game/levels.html", RequestContext(request, context))
