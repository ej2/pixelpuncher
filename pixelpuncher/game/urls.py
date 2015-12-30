from django.conf.urls import patterns, url

from pixelpuncher.game import views

urlpatterns = patterns(
    "",
    url(r'^skill/(?P<player_skill_id>[\w.@+-]+)/$', views.skill, name="skill"),
    url(r'^skip$', views.skip, name="skip"),
    url(r'^taunt$', views.taunt, name="taunt"),
    url(r'^play$', views.play, name="play"),
    url(r'^reset$', views.reset, name="reset"),
)
