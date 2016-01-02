from django.contrib import admin

from pixelpuncher.player.models import Player, Skill, PlayerSkill, Occupation


class PlayerModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "title", "level", "xp", "punches", "date_created", )
    search_fields = ("id", "name", "title", "level", "xp", "punches", "date_created",)
    raw_id_fields = ("user",)
    list_per_page = 25


class SkillModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hit_percentage", "critical_percentage", "energy_cost", )
    search_fields = ("id", "name", "hit_percentage", "critical_percentage", "energy_cost", )
    list_per_page = 25


class PlayerSkillModelAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "skill", "level", )
    search_fields = ("id", "level", )
    raw_id_fields = ("player",)
    list_per_page = 25


class OccupationModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "active", )
    search_fields = ("id", "name", )
    list_per_page = 25


admin.site.register(Player, PlayerModelAdmin)
admin.site.register(Skill, SkillModelAdmin)
admin.site.register(PlayerSkill, PlayerSkillModelAdmin)
admin.site.register(Occupation, OccupationModelAdmin)
