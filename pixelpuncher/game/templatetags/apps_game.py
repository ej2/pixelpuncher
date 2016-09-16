from __future__ import division
from django import template
from django.template.loader import render_to_string
from django.templatetags.static import static

from pixelpuncher.game.utils.game_settings import ADVENTURE_IMAGE_FOLDER
from pixelpuncher.game.utils.message import get_game_messages

register = template.Library()


@register.simple_tag()
def status_bar(label, current, total, css_class):
    percentage = (current / total) * 100

    return render_to_string("game/ui/bar.html", {
        "label": label,
        "current": current,
        "total": total,
        "percentage": percentage,
        "css_class": css_class
    })


@register.simple_tag()
def show_messages(player):
    game_messages = get_game_messages(player)

    return render_to_string("game/ui/messages.html", {
        "game_messages": game_messages,
    })


@register.simple_tag()
def adventure_image(adventure):
    if adventure.image_path:
        return static(ADVENTURE_IMAGE_FOLDER + adventure.image_path)
    else:
        return ""
