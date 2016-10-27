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

    url(r'^levels$', views.level_requirements, name="levels"),
    url(r'^level_up$', views.perform_level_up, name="level_up"),
    url(r'^cheatcode$', views.cheat_code, name="cheat_code"),
    url(r'^performcheat/(?P<cheatcode_id>[\w.@+-]+)$', views.perform_cheat, name="perform_cheat"),

    url(r'^(?P<locationservice_id>[\w.@+-]+)/pickfour/', include("pixelpuncher.game.urls.pickfour", namespace="pickfour")),

]
