from __future__ import division
from django import template
from django.template.loader import render_to_string

from pixelpuncher.game.utils.leveling import xp_required_for_level
from pixelpuncher.player.models import Player

register = template.Library()


@register.simple_tag()
def current_punches(user):
    player = Player.objects.get(user=user)

    return "Punches: {0} Health: {1} XP: {2}".format(
        player.punches, player.current_health, player.xp)


@register.simple_tag()
def mini_profile(user):
    player = Player.objects.get(user=user)

    return render_to_string("player/_mini_profile.html", {
        "player": player
    })


@register.simple_tag()
def display_current_next_xp(player):
    xp_next = int(xp_required_for_level(player.level))

    return "{0} / {1}".format(player.xp, xp_next)


@register.simple_tag()
def skill_list(player):

    return render_to_string("player/_skills.html", {
        "player": player,
        "skills": player.skills.all().order_by("skill__name")
    })
