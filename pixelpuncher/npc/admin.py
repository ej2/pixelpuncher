from django.contrib import admin

from pixelpuncher.npc.forms import CustomNPCAvatarForm
from pixelpuncher.npc.models import NPC, NPCAvatar, ResponseTrigger, Response, NPCRelationship, ResponseLog


class NPCModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level", )
    search_fields = ("id", "name", "level", )
    list_per_page = 50


class NPCAvatarModelAdmin(admin.ModelAdmin):
    form = CustomNPCAvatarForm
    list_display = ("id", "name", )
    search_fields = ("id", "name", )
    list_per_page = 50


class ResponseModelAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "xp_change", )
    search_fields = ("id", "text", "xp_change", )
    list_per_page = 50


class ResponseTriggerModelAdmin(admin.ModelAdmin):
    list_display = ("id", "trigger_text", "trigger_type", "response_handler")
    search_fields = ("id", "trigger_text", "trigger_type", )
    list_per_page = 50


class NPCRelationshipModelAdmin(admin.ModelAdmin):
    list_display = ("id", "npc", "player", "relationship_type", "relationship_level", "score",)
    search_fields = ("id", "npc", "player", "relationship_type", "relationship_level", "score",)
    list_per_page = 50


class ResponseLogModelAdmin(admin.ModelAdmin):
    list_display = ("id", "player", "response", "response_trigger", "response_date",)
    search_fields = ("id", "response_date",)
    list_per_page = 50


admin.site.register(NPC, NPCModelAdmin)
admin.site.register(NPCRelationship, NPCRelationshipModelAdmin)
admin.site.register(NPCAvatar, NPCAvatarModelAdmin)
admin.site.register(Response, ResponseModelAdmin)
admin.site.register(ResponseTrigger, ResponseTriggerModelAdmin)
admin.site.register(ResponseLog, ResponseLogModelAdmin)
