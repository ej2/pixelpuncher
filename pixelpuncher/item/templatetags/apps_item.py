from __future__ import division
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag()
def inventory_list(player):

    return render_to_string("player/_inventory.html", {
        "player": player,
        "items": player.items.all().order_by("item_type__name")
    })
