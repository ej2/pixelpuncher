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
def combat_skill_list(player):
    skills = player.skills.filter(skill__skill_type='ATTK').order_by("skill__name")

    if skills.count() > 0:
        return render_to_string("player/skills/_combat_skills.html", {
            "player": player,
            "skills": skills
        })
    else:
        return ""


@register.simple_tag()
def healing_skill_list(player):
    skills = player.skills.filter(skill__skill_type='HEAL').order_by("skill__name")

    if skills.count() > 0:
        return render_to_string("player/skills/_healing_skills.html", {
            "player": player,
            "skills": skills
        })
    else:
        return ""


@register.simple_tag()
def passive_skill_list(player):
    skills = player.skills.filter(skill__skill_type='PASS').order_by("skill__name")

    if skills.count() > 0:
        return render_to_string("player/skills/_passive_skills.html", {
            "player": player,
            "skills": skills
        })
    else:
        return ""


@register.simple_tag()
def avatar(player):
    return render_to_string("player/_avatar_display.html", {
        "player": player,
    })


@register.simple_tag()
def small_avatar(player):
    return render_to_string("player/_avatar_small_display.html", {
        "player": player,
    })

