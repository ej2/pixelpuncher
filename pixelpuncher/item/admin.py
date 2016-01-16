from django.contrib import admin

from pixelpuncher.item.models import ItemType, Item, DropTable, ItemDrop, LevelEquipment


class ItemTypeModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "classification", "base_type", "level_requirement", "description")
    search_fields = ("id", "name", "classification")
    list_per_page = 50


class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("id", "item_type", "player", "remaining_uses",)
    search_fields = ("id", "item_type", "player", "remaining_uses",)
    list_per_page = 25


class DropTableModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "recommended_level", "max_drops", "max_rate")
    search_fields = ("id", "name", "recommended_level", "max_rate")
    list_per_page = 25


class ItemDropModelAdmin(admin.ModelAdmin):
    list_display = ("id", "drop_table", "item_type", "drop_rate")
    search_fields = ("id", "drop_table__name", "item_type__name", "drop_rate")
    list_per_page = 25


class LevelEquipmentModelAdmin(admin.ModelAdmin):
    list_display = ("id", "item_type", "level")
    search_fields = ("id", "item_type", "level")
    list_per_page = 25


admin.site.register(ItemType, ItemTypeModelAdmin)
admin.site.register(Item, ItemModelAdmin)
admin.site.register(DropTable, DropTableModelAdmin)
admin.site.register(ItemDrop, ItemDropModelAdmin)
admin.site.register(LevelEquipment, LevelEquipmentModelAdmin)
