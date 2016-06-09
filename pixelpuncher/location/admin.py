from django.contrib import admin

from pixelpuncher.location.models import Location, LocationItem, Service, LocationService


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


class ServiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "service_type", "min_amount", "max_amount",)
    search_fields = ("id", "name", "service_type", "min_amount", "max_amount",)
    list_per_page = 50


class LocationServiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "location", "service", "price",)
    search_fields = ("id", "location", "service", "price",)
    raw_id_fields = ("service",)
    list_per_page = 50


admin.site.register(Location, LocationModelAdmin)
admin.site.register(LocationItem, LocationItemsModelAdmin)
admin.site.register(Service, ServiceModelAdmin)
admin.site.register(LocationService, LocationServiceModelAdmin)
