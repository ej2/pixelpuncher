from django.contrib import admin

from pixelpuncher.npc.forms import CustomNPCAvatarForm
from pixelpuncher.npc.models import NPC, NPCAvatar


class NPCModelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "level", )
    search_fields = ("id", "name", "level", )
    list_per_page = 50


class NPCAvatarModelAdmin(admin.ModelAdmin):
    form = CustomNPCAvatarForm
    list_display = ("id", "name", )
    search_fields = ("id", "name", )
    list_per_page = 50


admin.site.register(NPC, NPCModelAdmin)
admin.site.register(NPCAvatar, NPCAvatarModelAdmin)
