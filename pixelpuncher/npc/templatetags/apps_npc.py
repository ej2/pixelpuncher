from __future__ import division
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag()
def npc_profile(npc):
    return render_to_string("npc/_npc_profile.html", {
        "npc": npc
    })


@register.simple_tag()
def npc_avatar(npc):
    return render_to_string("npc/_avatar_display.html", {
        "npc": npc,
    })
