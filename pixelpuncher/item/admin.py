from django.contrib import admin

from pixelpuncher.item.models import ItemType, Item, DropTable, ItemDrop


class ItemTypeModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "classification", "base_type", "description")
    search_fields = ("id", "name", "classification")
    list_per_page = 25


class ItemModelAdmin(admin.ModelAdmin):
    list_display = ("id", "item_type", "player", "remaining_uses",)
    search_fields = ("id", "item_type", "player", "remaining_uses",)
    list_per_page = 25


class DropTableModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "max_rate")
    search_fields = ("id", "name", "max_rate")
    list_per_page = 25


class ItemDropModelAdmin(admin.ModelAdmin):
    list_display = ("id", "drop_table", "item_type", "drop_rate")
    search_fields = ("id", "drop_table", "item_type", "drop_rate")
    list_per_page = 25


admin.site.register(ItemType, ItemTypeModelAdmin)
admin.site.register(Item, ItemModelAdmin)
admin.site.register(DropTable, DropTableModelAdmin)
admin.site.register(ItemDrop, ItemDropModelAdmin)
