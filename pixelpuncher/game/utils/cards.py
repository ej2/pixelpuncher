import random

from pixelpuncher.game.models import MatchGame, MatchCard, CardType, GameState

ONE_CARDS = 5
TWO_CARDS = 3
FOUR_CARDS = 2
EIGHT_CARDS = 1
BOMB_CARDS = 4
SPECIAL_CARDS = 1


def start_match_game(player):
    game = MatchGame(player=player)
    game.save()

    for c in range(0, ONE_CARDS):
        add_card(game, CardType.ONE)

    for c in range(0, TWO_CARDS):
        add_card(game, CardType.TWO)

    for c in range(0, FOUR_CARDS):
        add_card(game, CardType.FOUR)

    for c in range(0, EIGHT_CARDS):
        add_card(game, CardType.EIGHT)

    for c in range(0, BOMB_CARDS):
        add_card(game, CardType.BOMB)

    for c in range(0, SPECIAL_CARDS):
        add_card(game, CardType.SPECIAL)

    shuffle(game)
    return game


def add_card(game, card_type):
    card = MatchCard(card_type=card_type)
    card.game = game
    card.save()

    return card


def shuffle(match_game):
    for position in range(1, match_game.cards.all().count() + 1):
        card = random.choice(match_game.cards.filter(position=0))
        card.position = position
        card.save()


def get_points(card):
    points = {
        CardType.ONE: 1,
        CardType.TWO: 2,
        CardType.FOUR: 4,
        CardType.EIGHT: 8,
        CardType.SPECIAL: -1,
        CardType.BOMB: 0,
    }

    return points.get(card.card_type) * card.game.multiplier


def get_card_message(card):
    card_msg = {
        CardType.ONE: "Meh.",
        CardType.TWO: "Two points.",
        CardType.FOUR: "Four points!",
        CardType.EIGHT: "SWEEET! Eight points!",
        CardType.SPECIAL: "DOUBLE SCORE!!!!",
        CardType.BOMB: "A big nothing...",
    }

    return card_msg.get(card.card_type)


def update_game_state(match_game):
    if match_game.cards.filter(flipped=True).count() == 4:
        match_game.state = GameState.GAME_OVER
        match_game.save()


def reward_player(match_game, player):
    player.pixels += match_game.points
    player.save()
