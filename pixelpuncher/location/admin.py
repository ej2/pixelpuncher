from django.contrib import admin

from pixelpuncher.location.models import Location, LocationItem


class LocationModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "location_type",)
    search_fields = ("id", "name", "location_type",)
    raw_id_fields = ("players",)
    list_per_page = 50


class LocationItemsModelAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "item_type", "price",)
    search_fields = ("id", "location", "item_type", "price",)
    raw_id_fields = ("item_type",)
    list_per_page = 50

admin.site.register(Location, LocationModelAdmin)
admin.site.register(LocationItem, LocationItemsModelAdmin)
