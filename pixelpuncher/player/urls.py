from django.conf.urls import patterns, url

from pixelpuncher.player import views

urlpatterns = patterns(
    "",
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
    url(r'^drop/(?P<item_id>[\w.@+-]+)/$', views.drop, name="drop"),
    url(r'^use/(?P<item_id>[\w.@+-]+)/$', views.use, name="use"),
)
