from django.contrib import admin

from pixelpuncher.player.models import Player, Skill, PlayerSkill, Occupation, Avatar, PlayerAvatar, AvatarLayer


class PlayerModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "user", "title", "level", "xp", "punches", "date_created", )
    search_fields = ("id", "name", "title", "level", "xp", "punches", "date_created",)
    raw_id_fields = ("user",)
    list_per_page = 25


class AvatarLayerModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "gender", "layer_type", "unlock_method", "image_path", "active",)
    search_fields = ("id", "image_path", "active",)
    list_per_page = 25


class PlayerAvatarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "layer", "current",)
    search_fields = ("id", "date_created",)
    raw_id_fields = ("player", "layer",)
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


class AvatarModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "gender", "image_path", "active",)
    search_fields = ("id", "image_path", "active",)
    list_per_page = 25


admin.site.register(Avatar, AvatarModelAdmin)
admin.site.register(AvatarLayer, AvatarLayerModelAdmin)
admin.site.register(PlayerAvatar, PlayerAvatarModelAdmin)
admin.site.register(Player, PlayerModelAdmin)
admin.site.register(Skill, SkillModelAdmin)
admin.site.register(PlayerSkill, PlayerSkillModelAdmin)
admin.site.register(Occupation, OccupationModelAdmin)
