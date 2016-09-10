from django.conf.urls import url

from pixelpuncher.player import views

urlpatterns = [
    url(r'^new$', views.PlayerCreateView.as_view(), name="new"),
    url(r'^redirect$', views.player_redirect, name="redirect"),
    url(
        regex=r'^(?P<player_id>[\w.@+-]+)/$',
        view=views.PlayerDetailView.as_view(),
        name='detail'
    ),
    url(
        regex=r'^(?P<player_id>[\w.@+-]+)/spend$',
        view=views.AttributeSpendView.as_view(),
        name='spend'
    ),
    url(r'^avatar_choose/(?P<avatar_id>[\w.@+-]+)/$', views.choose_avatar, name='avatar_choose'),
    url(r'^avatar', views.avatar_list, name='avatar'),
    url(r'^achievements', views.view_achievements, name='achievements'),
    url(r'^examine/(?P<item_id>[\w.@+-]+)/$', views.examine, name="examine"),
    url(r'^drop/(?P<item_id>[\w.@+-]+)/$', views.drop, name="drop"),
    url(r'^use/(?P<item_id>[\w.@+-]+)/$', views.use, name="use"),
    url(r'^skill/(?P<player_skill_id>[\w.@+-]+)/$', views.skill, name="skill"),

    url(r'^top_punchers$', views.top_punchers, name="top_punchers"),
]
