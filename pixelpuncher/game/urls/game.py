from django.conf.urls import url, include

from pixelpuncher.game.views import views
from pixelpuncher.game.views.games import pickfour

urlpatterns = [
    url(r'^skill/(?P<player_skill_id>[\w.@+-]+)/$', views.skill, name="skill"),
    url(r'^use/(?P<item_id>[\w.@+-]+)/$', views.use, name="use"),
    url(r'^skip$', views.skip, name="skip"),
    url(r'^taunt$', views.taunt, name="taunt"),
    url(r'^start$', views.game_start, name="start"),
    url(r'^play$', views.play, name="play"),
    url(r'^choice/(?P<choice_id>[\w.@+-]+)/$', views.adventure_choice, name="choice"),
    url(r'^map$', views.map, name="map"),
    url(r'^reset$', views.reset, name="reset"),

    url(r'^levels$', views.level_requirements, name="levels"),
    url(r'^daily_reset$', views.perform_daily_reset, name="daily_reset"),
    url(r'^level_up$', views.perform_level_up, name="level_up"),

    url(r'^(?P<locationservice_id>[\w.@+-]+)/pickfour/', include("pixelpuncher.game.urls.pickfour", namespace="pickfour")),

]