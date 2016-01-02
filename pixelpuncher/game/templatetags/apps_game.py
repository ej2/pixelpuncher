from __future__ import division
from django import template
from django.template.loader import render_to_string


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
