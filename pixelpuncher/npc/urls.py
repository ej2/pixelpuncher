from django.conf.urls import url

from pixelpuncher.npc import views

urlpatterns = [
    url(r'^talk/(?P<location_id>[\w.@+-]+)$', views.talk, name="talk"),
]
