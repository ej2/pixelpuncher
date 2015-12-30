from django.contrib import admin

from pixelpuncher.game.models import GameMessage


class GameMessageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "message", "shown", "date_created", )
    search_fields = ("id", "message", "date_created",)
    raw_id_fields = ("player",)
    list_per_page = 25

admin.site.register(GameMessage, GameMessageModelAdmin)
