from django.conf.urls import url

from pixelpuncher.npc import views

urlpatterns = [
    url(r'^(?P<location_id>[\w.@+-]+)/talk/(?P<npc_id>[\w.@+-]+)$', views.talk, name="talk"),
    url(r'^(?P<location_id>[\w.@+-]+)/punch/(?P<npc_id>[\w.@+-]+)$', views.punch, name="punch"),
    url(r'^(?P<location_id>[\w.@+-]+)/chatter/(?P<npc_id>[\w.@+-]+)$', views.chatter, name="chatter"),
    url(r'^(?P<location_id>[\w.@+-]+)/train/(?P<npc_id>[\w.@+-]+)$', views.train, name="train"),
]
