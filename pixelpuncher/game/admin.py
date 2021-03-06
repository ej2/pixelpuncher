from django.contrib import admin

from pixelpuncher.game.models import GameMessage, MatchGame, CheatCode


class MatchGameModelAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "date_created", "state", )
    search_fields = ("id", "date_created",)
    raw_id_fields = ("player",)
    list_per_page = 50


class GameMessageModelAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "message", "shown", "date_created", )
    search_fields = ("id", "message", "date_created",)
    raw_id_fields = ("player",)
    list_per_page = 25


class CheatCodeModelAdmin(admin.ModelAdmin):
    list_display = ("code", "cheat_class", "admin_only", "date_created",)
    search_fields = ("code", "cheat_class", "admin_only",)
    list_per_page = 50

admin.site.register(GameMessage, GameMessageModelAdmin)
admin.site.register(CheatCode, CheatCodeModelAdmin)
admin.site.register(MatchGame, MatchGameModelAdmin)
