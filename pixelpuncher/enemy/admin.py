from django.contrib import admin

from pixelpuncher.enemy.models import EnemyCategory, EnemyType, Enemy


class EnemyCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("code", "name", )
    search_fields = ("code", "name", )
    list_per_page = 25


class EnemyTypeCategoryModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "xp", "base_level", "maximum_health", "date_created",)
    search_fields = ("id", "name", "category", "xp", "base_level", "date_created", )
    list_per_page = 25


class EnemyModelAdmin(admin.ModelAdmin):
    list_display = ("id", "enemy_type", "active", "player", "current_health", "date_created",)
    search_fields = ("id", "current_health", "active", "date_created",)
    list_per_page = 25


admin.site.register(EnemyCategory, EnemyCategoryModelAdmin)
admin.site.register(EnemyType, EnemyTypeCategoryModelAdmin)
admin.site.register(Enemy, EnemyModelAdmin)
