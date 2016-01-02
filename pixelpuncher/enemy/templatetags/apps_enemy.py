from __future__ import division
from django import template
from django.template.loader import render_to_string
from django.templatetags.static import static

from pixelpuncher.game.utils.game_settings import ENEMY_IMAGE_FOLDER

register = template.Library()


@register.simple_tag()
def enemy_mini_profile(enemy):
    health_bar_percent = ((enemy.current_health / enemy.total_health) * 100)

    return render_to_string("enemy/_mini_profile.html", {
        "enemy": enemy,
        "health_bar_percent": health_bar_percent
    })


@register.simple_tag()
def enemy_image_path(enemy):
    if enemy.enemy_type.image_name:
        return static(ENEMY_IMAGE_FOLDER + enemy.enemy_type.image_name)
    else:
        return static(ENEMY_IMAGE_FOLDER + "darkness.png")
