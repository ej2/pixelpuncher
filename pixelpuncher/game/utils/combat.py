from __future__ import division

import random

from pixelpuncher.game.utils.calculations import calculate_hit, calculate_critial_hit, calculate_critial_damage, \
    calculate_damage, calculate_enemy_damage, calculate_enemy_hit, percentage_roll, dice_roll
from pixelpuncher.game.utils.encounter import get_current_enemy
from pixelpuncher.game.utils.game_settings import TAUNT_SUCCESS_PERCENTAGE, TAUNT_EPIC_SUCCESS_PERCENTAGE
from pixelpuncher.game.utils.leveling import can_level_up, level_up
from pixelpuncher.game.utils.loot import generate_loot, generate_pixels
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import successful_critical_message, successful_hit_message, low_energy_message, \
    hit_failure_message, player_damage_message, successful_heal_message, failed_heal_message, victory_message, \
    battle_message, xp_gained_message, bonus_xp_gained_message, run_away_message
from pixelpuncher.item.utils import use_item
from pixelpuncher.player.models import VICTORY


def perform_skill(player, player_skill):
    if can_use_skill(player, player_skill):
        if player_skill.skill.skill_type == "HEAL":
            results = perform_heal_skill(player, player_skill)

            # Process results
            if results['success']:
                player.adjust_health(results['amount'])
                add_game_message(
                    player, successful_heal_message(player_skill.skill, results['amount']))
            else:
                add_game_message(
                    player, failed_heal_message(player_skill.skill))

        # Apply player changes
        player.adjust_energy(-player_skill.energy_cost)
        player.save()


def perform_skill_in_combat(player, player_skill):
    victory = False
    enemy = get_current_enemy(player)
    add_game_message(player, battle_message(enemy))

    if can_use_skill(player, player_skill):

        if player_skill.skill.skill_type == "ATTK":
            results = perform_attack_skill(player, enemy, player_skill)

            # Process results
            if results['hit']:
                enemy.hits += 1
                if results['critical']:
                    enemy.adjust_health(-results['critical_damage'])
                    add_game_message(
                        player, successful_critical_message(player_skill.skill, enemy, results['critical_damage']))
                else:
                    enemy.adjust_health(-results['damage'])
                    add_game_message(
                        player, successful_hit_message(player_skill.skill, enemy, results['damage']))
            else:
                add_game_message(player, hit_failure_message(player_skill.skill, enemy))

        elif player_skill.skill.skill_type == "SPCL":
            results = perform_special_skill(player, enemy, player_skill)

        elif player_skill.skill.skill_type == "HEAL":
            results = perform_heal_skill(player, player_skill)

            # Process results
            if results['success']:
                player.adjust_health(results['amount'])
                add_game_message(
                    player, successful_heal_message(player_skill.skill, results['amount']))
            else:
                add_game_message(
                    player, failed_heal_message(player_skill.skill))

        if enemy.is_defeated:
            victory = True
            player.status = VICTORY
        else:
            perform_enemy_attack(player, enemy)

        # Apply player changes
        player.adjust_energy(-player_skill.energy_cost)

        player.save()
        enemy.save()

    else:
        add_game_message(player, low_energy_message(player_skill.skill))

    if victory:
        add_game_message(player, victory_message())
        generate_loot(player, enemy)
        generate_pixels(player, enemy)
        calculate_xp(player, enemy)

    return victory


def perform_enemy_attack(player, enemy):
    hit = calculate_enemy_hit(player, enemy)

    if hit:
        damage = calculate_enemy_damage(enemy)
        player.adjust_health(-damage)
        add_game_message(player, player_damage_message(damage))


def perform_special_skill(player, enemy, player_skill):
    # TODO: Finish
    damage = 0
    critical_damage = 0

    hit = False
    critical = False

    return {
        "hit": hit,
        "damage": damage,
        "critical": critical,
        "critical_damage": critical_damage,
    }


def perform_heal_skill(player, player_skill):
    heal_amount = 0

    success = percentage_roll(player_skill.hit_percentage)
    if success:
        heal_amount = dice_roll(player_skill.number_of_dice, player_skill.dice_sides, player_skill.bonus)

    return {
        "success": success,
        "amount": heal_amount,
    }


def perform_attack_skill(player, enemy, player_skill):
    damage = 0
    critical_damage = 0

    hit = calculate_hit(player, enemy, player_skill.hit_percentage)
    critical = False

    if hit:
        # Calculate damage
        damage = calculate_damage(player, player_skill)

        if player_skill.critical_percentage > 0:
            critical = calculate_critial_hit(player, player_skill.critical_percentage)

            if critical:
                critical_damage = calculate_critial_damage(damage, player_skill.critical_multipler, player.power)

    return {
        "hit": hit,
        "damage": damage,
        "critical": critical,
        "critical_damage": critical_damage,
    }


def can_use_skill(player, player_skill):
    if player.current_energy >= player_skill.energy_cost:
        return True
    return False


def perform_taunt(player):
    enemy = get_current_enemy(player)
    add_game_message(player, battle_message(enemy))

    taunt_success = random.randint(1, 100)

    if taunt_success < TAUNT_EPIC_SUCCESS_PERCENTAGE:
        player.adjust_energy(random.randint(10, 20))
        player.save()

        result = "You taunt and call the {0} names. Ohhhh burn! You feel a lot better about yourself.".format(
            enemy.enemy_type.name)

    elif taunt_success < TAUNT_SUCCESS_PERCENTAGE:
        player.adjust_energy(random.randint(1, 4))
        player.save()

        result = "You taunt and call the {0} names. You feel better about yourself but it does not respond.".format(
            enemy.enemy_type.name)
    else:
        result = "You taunt and call the {0} names, then realize it doesn't care. ".format(
            enemy.enemy_type.name)

    add_game_message(player, result)


def perform_skip(player):
    enemy = get_current_enemy(player)
    enemy.active = False
    enemy.save()

    result = run_away_message(enemy.enemy_type.name)
    add_game_message(player, result)


def perform_use_item(player, item_id):
    enemy = get_current_enemy(player)

    result = use_item(player, item_id)
    add_game_message(player, result)

    perform_enemy_attack(player, enemy)
    player.save()


def calculate_xp(player, enemy):
    gained_xp = enemy.enemy_type.xp
    player.xp += gained_xp

    result = xp_gained_message(gained_xp)
    add_game_message(player, result)

    if enemy.hits == 1:
        # Bonus XP
        bonus_xp = int(enemy.enemy_type.xp / 2 + enemy.level)

        player.xp += bonus_xp
        result = bonus_xp_gained_message('Single hit kill!', bonus_xp)
        add_game_message(player, result)

    if can_level_up(player):
        level_up(player)

    player.save()
