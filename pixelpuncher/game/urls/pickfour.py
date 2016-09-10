from django.conf.urls import url

from pixelpuncher.game.views.games import pickfour

urlpatterns = [
    url(r'^start$', pickfour.start_game, name="start-game"),
    url(r'^play$', pickfour.card_game, name="card"),
    url(r'^flip/(?P<game_id>[\w.@+-]+)/(?P<card_id>[\w.@+-]+)$', pickfour.flip, name="flip"),
]
