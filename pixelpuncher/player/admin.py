from django.contrib import admin

from pixelpuncher.player.models import Player, Skill, PlayerSkill, Occupation, Avatar, PlayerAvatar, AvatarLayer, \
    Achievement, Collection, PlayerCollection


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
    list_per_page = 50


class AchievementModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "icon",)
    search_fields = ("id", "name", "description", "icon",)
    list_per_page = 50


class CollectionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "achievement", "date_created",)
    search_fields = ("id", "name", "achievement__name", "date_created",)
    list_per_page = 50


class PlayerCollectionModelAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "collection", "date_created",)
    search_fields = ("id", "player", "collection", "date_created",)
    list_per_page = 50


admin.site.register(Achievement, AchievementModelAdmin)
admin.site.register(Avatar, AvatarModelAdmin)
admin.site.register(AvatarLayer, AvatarLayerModelAdmin)
admin.site.register(PlayerAvatar, PlayerAvatarModelAdmin)
admin.site.register(Player, PlayerModelAdmin)
admin.site.register(Skill, SkillModelAdmin)
admin.site.register(PlayerSkill, PlayerSkillModelAdmin)
admin.site.register(Occupation, OccupationModelAdmin)
admin.site.register(Collection, CollectionModelAdmin)
admin.site.register(PlayerCollection, PlayerCollectionModelAdmin)
