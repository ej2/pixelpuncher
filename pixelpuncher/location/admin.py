from django.contrib import admin

from pixelpuncher.location.models import Location, LocationItem, Service, LocationService, Adventure, AdventureChoice


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


class AdventureModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "frequency",)
    search_fields = ("id", "title", )
    list_per_page = 50


class AdventureChoiceModelAdmin(admin.ModelAdmin):
    list_display = ("id", "adventure", "option_text", "success_percentage",)
    search_fields = ("id", "adventure__title", "option_text", "success_percentage",)
    list_per_page = 50


admin.site.register(Location, LocationModelAdmin)
admin.site.register(LocationItem, LocationItemsModelAdmin)
admin.site.register(Service, ServiceModelAdmin)
admin.site.register(LocationService, LocationServiceModelAdmin)
admin.site.register(Adventure, AdventureModelAdmin)
admin.site.register(AdventureChoice, AdventureChoiceModelAdmin)
