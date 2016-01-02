from __future__ import division

import random

from pixelpuncher.game.utils.calculations import calculate_hit, calculate_critial_hit, calculate_critial_damage, \
    calculate_damage, calculate_enemy_damage, calculate_enemy_hit, percentage_roll, dice_roll
from pixelpuncher.game.utils.encounter import get_current_enemy
from pixelpuncher.game.utils.leveling import can_level_up, level_up
from pixelpuncher.game.utils.loot import generate_loot
from pixelpuncher.game.utils.message import add_game_message
from pixelpuncher.game.utils.messages import successful_critical_message, successful_hit_message, low_energy_message, \
    hit_failure_message, player_damage_message, successful_heal_message, failed_heal_message
from pixelpuncher.player.models import VICTORY


def perform_skill(player, player_skill):
    victory = False
    enemy = get_current_enemy(player)

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

        elif player_skill.skill.skill_type == "SPCL":
            results = perform_special_skill(player, enemy, player_skill)

        elif player_skill.skill.skill_type == "HEAL":
            results = perform_heal_skill(player, enemy, player_skill)

            # Process results
            if results['success']:
                player.adjust_health(results['amount'])
                add_game_message(
                    player, successful_heal_message(player_skill.skill, results['amount']))
            else:
                add_game_message(
                    player, failed_heal_message(player_skill.skill))

        else:
            add_game_message(player, hit_failure_message(player_skill.skill, enemy))

        if enemy.is_defeated:
            victory = True
            player.status = VICTORY
        else:
            attack_results = perform_enemy_attack(player, enemy)

            if attack_results['hit']:
                player.adjust_health(-attack_results['damage'])
                add_game_message(player, player_damage_message(attack_results['damage']))

        # Apply player changes
        player.adjust_energy(-player_skill.energy_cost)
        player.punches -= 1  # Should each attack cost one punch or each combat?

        player.save()
        enemy.save()

    else:
        add_game_message(player, low_energy_message(player_skill.skill))

    if victory:
        generate_loot(player, enemy)
        calculate_xp(player, enemy)

    return victory


def perform_enemy_attack(player, enemy):
    hit = calculate_enemy_hit(player, enemy)
    damage = 0

    if hit:
        damage = calculate_enemy_damage(enemy)

    return {
        "hit": hit,
        "damage": damage,
    }


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


def perform_heal_skill(player, enemy, player_skill):
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
    player.adjust_energy(random.randint(1, 4))
    player.save()

    result = "You taunt and call the {0} names. You feel better about yourself but it does not respond.".format(
        enemy.enemy_type.name)

    add_game_message(player, result)


def perform_skip(player):
    enemy = get_current_enemy(player)
    enemy.active = False
    enemy.save()

    result = "You don't want to punch a stupid {0}.".format(enemy.enemy_type.name)
    add_game_message(player, result)


def calculate_xp(player, enemy):
    gained_xp = enemy.enemy_type.xp
    player.xp += gained_xp

    result = "<span class='xp'>+{0}XP!</span>".format(gained_xp)
    add_game_message(player, result)

    if enemy.hits == 1:
        # Bonus XP
        bonus_xp = int(enemy.enemy_type.xp / 2 + enemy.level)

        player.xp += bonus_xp
        result = "<span class='xp'>Single hit kill! Bonus +{0}XP!</span>".format(bonus_xp)
        add_game_message(player, result)

    if can_level_up(player):
        level_up(player)

    player.save()
