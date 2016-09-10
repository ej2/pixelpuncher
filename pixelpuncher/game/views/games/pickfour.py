from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.template.response import TemplateResponse

from pixelpuncher.game.models import MatchGame, MatchCard, GameState, CardType
from pixelpuncher.game.utils.cards import start_match_game, get_points, update_game_state, reward_player, \
    get_card_message
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.location.models import LocationService
from pixelpuncher.npc.utils.relationships import get_relationship
from pixelpuncher.player.decorators import player_required


@login_required
@player_required
def card_game(request, player, locationservice_id):
    match_game = get_object_or_None(MatchGame, player=player, state='PLAY')
    location_service = get_object_or_404(LocationService, id=locationservice_id)
    location = location_service.location

    if match_game is None:
        match_game = get_object_or_None(MatchGame, player=player, state='OVER')

        if match_game:
            match_game.state = GameState.CLOSED
            match_game.save()
        else:
            return redirect("game:pickfour:start-game", locationservice_id)

    if location.npc:
        relationship = get_relationship(player, location.npc)
    else:
        relationship = None

    context = {
        "user": player.user,
        "player": player,
        "match_game": match_game,
        "cards": match_game.cards.order_by('position'),
        "locationservice_id": locationservice_id,
        "location": location,
        "relationship": relationship,
    }

    return TemplateResponse(
        request, "game/pickfour/card.html", RequestContext(request, context))


@login_required
@player_required
def flip(request, player, locationservice_id, game_id, card_id):
    card = get_object_or_404(MatchCard, game_id=game_id, id=card_id)
    card.flipped = True
    card.save()

    if card.card_type != CardType.SPECIAL:
        card.game.points += get_points(card)
    else:
        card.game.multiplier = 2
        card.game.points *= card.game.multiplier

    card.game.save()

    match_game = get_object_or_None(MatchGame, id=card.game.id)
    update_game_state(match_game)

    if match_game.state == GameState.GAME_OVER:
        reward_player(match_game, player)
        add_game_message(player, "You win {} pixels!".format(match_game.points))
    else:
        add_game_message(player, "You flip a card. {}".format(get_card_message(card)))

    return redirect("game:pickfour:card", locationservice_id)


@login_required
@player_required
def start_game(request, player, locationservice_id):
    start_match_game(player)
    player.pixels -= 5  # cost of playing game
    player.save()

    add_game_message(player, "You pay 5 pixels to play Pick 4.")
    return redirect("game:pickfour:card", locationservice_id)
