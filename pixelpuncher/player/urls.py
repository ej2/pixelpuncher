from django.conf.urls import patterns, url

from pixelpuncher.player import views

urlpatterns = patterns(
    "",
    url(r'^new$', views.PlayerCreateView.as_view(), name="new"),
    url(
        regex=r'^(?P<player_id>[\w.@+-]+)/$',
        view=views.PlayerDetailView.as_view(),
        name='detail'
    ),
    url(r'^drop/(?P<item_id>[\w.@+-]+)/$', views.drop, name="drop"),
    url(r'^use/(?P<item_id>[\w.@+-]+)/$', views.use, name="use"),
)
