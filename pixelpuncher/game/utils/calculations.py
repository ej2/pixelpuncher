import random


def calculate_critial_damage(damage, multipler, bonus):
    return damage * multipler + bonus


def calculate_critial_hit(player, critical_percent):
    crit_chance = critical_percent + player.technique
    return percentage_roll(crit_chance)


def calculate_hit(player, enemy, hit_rate):
    chance_of_hit = hit_rate + player.technique - enemy.defense
    return percentage_roll(chance_of_hit)


def calculate_damage(player, player_skill):
    damage = dice_roll(player_skill.number_of_dice, player_skill.dice_sides, player_skill.bonus)
    return damage + player.power


def calculate_enemy_hit(player, enemy):
    """
    Basic calculation to see if the enemy hits.
    :param player:
    :param enemy:
    :return:
    """
    chance_of_hit = enemy.attack - player.effective_armor
    return percentage_roll(chance_of_hit)


def calculate_enemy_damage(enemy):
    return dice_roll(enemy.number_of_dice, enemy.dice_sides, enemy.bonus)


def percentage_roll(chance):
    if random.randint(1, 100) < chance:
        return True

    return False


def dice_roll(number_of_dice, sides, bonus=0):
    result = bonus
    for x in range(0, number_of_dice):
        result += random.randint(1, sides)

    return result
