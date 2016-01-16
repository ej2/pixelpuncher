from django.conf.urls import patterns, url

from pixelpuncher.game import views

urlpatterns = patterns(
    "",
    url(r'^skill/(?P<player_skill_id>[\w.@+-]+)/$', views.skill, name="skill"),
    url(r'^use/(?P<item_id>[\w.@+-]+)/$', views.use, name="use"),
    url(r'^skip$', views.skip, name="skip"),
    url(r'^taunt$', views.taunt, name="taunt"),
    url(r'^start$', views.game_start, name="start"),
    url(r'^play$', views.play, name="play"),
    url(r'^reset$', views.reset, name="reset"),

    url(r'^levels$', views.level_requirements, name="levels"),
    url(r'^daily_reset$', views.perform_daily_reset, name="daily_reset"),

)
