from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import learned_skill_message
from pixelpuncher.player.models import PlayerSkill, Skill


def add_starting_skills(player):
    skills = Skill.objects.filter(level=1)

    for skill in skills:
        create_player_skill(player, skill)


def add_skills(player, level):
    skills = Skill.objects.filter(level=level)

    for skill in skills:
        create_player_skill(player, skill)
        add_game_message(player, learned_skill_message(skill))


def create_player_skill(player, skill):
    player_skill = PlayerSkill()
    player_skill.skill = skill
    player_skill.player = player
    player_skill.hit_percentage = skill.hit_percentage
    player_skill.critical_percentage = skill.critical_percentage
    player_skill.critical_multipler = skill.critical_multipler
    player_skill.energy_cost = skill.energy_cost
    player_skill.number_of_dice = skill.number_of_dice
    player_skill.dice_sides = skill.dice_sides
    player_skill.bonus = skill.bonus
    player_skill.remaining_for_level_up = skill.gain_frequency

    player_skill.save()

    return player_skill


def level_skill(player_skill):
    level_up = False
    player_skill.remaining_for_level_up -= 1

    if player_skill.remaining_for_level_up == 0:
        level_up = True
        player_skill.level += 1
        player_skill.hit_percentage += player_skill.skill.gained_hit
        player_skill.critical_percentage += player_skill.skill.gained_critical
        player_skill.critical_multipler += player_skill.skill.gained_critical_multipler
        player_skill.energy_cost += player_skill.skill.gained_energy_cost
        player_skill.bonus += player_skill.skill.gained_bonus
        player_skill.remaining_for_level_up = player_skill.skill.gain_frequency

    player_skill.save()
    return level_up
