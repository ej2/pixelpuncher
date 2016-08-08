from django.conf.urls import url

from pixelpuncher.npc import views

urlpatterns = [
    url(r'^(?P<location_id>[\w.@+-]+)/talk/(?P<npc_id>[\w.@+-]+)$', views.talk, name="talk"),
    url(r'^(?P<location_id>[\w.@+-]+)/punch/(?P<npc_id>[\w.@+-]+)$', views.punch, name="punch"),
]
