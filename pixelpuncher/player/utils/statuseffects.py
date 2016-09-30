from pixelpuncher.player.models import PlayerStatusEffect


def add_status_effect(player, status_effect, duration):
    player_status_effect = PlayerStatusEffect.objects.get_or_create(player=player, status_effect=status_effect)
    player_status_effect.remaining_turns += duration
    player_status_effect.save()

    return player_status_effect
