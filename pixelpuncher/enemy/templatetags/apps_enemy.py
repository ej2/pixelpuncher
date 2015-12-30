from __future__ import division
from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag()
def enemy_mini_profile(enemy):
    health_bar_percent = ((enemy.current_health / enemy.total_health) * 100)

    return render_to_string("enemy/_mini_profile.html", {
        "enemy": enemy,
        "health_bar_percent": health_bar_percent
    })
