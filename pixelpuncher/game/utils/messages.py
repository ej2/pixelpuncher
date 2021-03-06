import random

from pixelpuncher.game.utils.message import GameMessageManager, get_random_attack_verbs, get_random_pain_word, \
    get_random_defeat_message

DANGER_WORDS = ["treacherous", "formidable", "deadly", "troublesome", "lethal"]


def low_energy_message(skill):
    return "<span class='hit'>You don't have enough energy to perform {0}!</span> ".format(skill.name)


def successful_hit_message(skill, enemy, damage):
    return "You {0} the {1} and hit for <span class='hit'>{2} damage</span>! ".format(
        skill.name, enemy, int(damage))


def successful_critical_message(skill, enemy, damage):
    hit_message = successful_hit_message(skill, enemy, damage)
    return "{0}<span class='critial'>CRITIAL HIT!</span> ".format(hit_message)


def hit_failure_message(skill, enemy):
    return "<span class='miss'>You try to {0} the {1} and miss!</span> ".format(skill.name, enemy)


def victory_message():
    return "<span class='victory'>Victory!</span> "


def player_damage_message(enemy, damage):
    return "The {} {} at you. {} You lose <span class='health'>{} health</span>. ".format(
        enemy.enemy_type.name, get_random_attack_verbs(), get_random_pain_word(), int(damage))


def enemy_hit_failure(enemy):
    return "The {} {} at you and misses!".format(enemy.enemy_type.name, get_random_attack_verbs())


def player_level_up_message():
    return "<span class='level-up'>LEVEL UP!</span> "


def learned_skill_message(skill):
    return "You learned <span class='skill'>{0}</span>! ".format(skill.name)


def successful_heal_message(skill, amount):
    return "You use {0} and are healed for <span class='health'>{1} health</span>. ".format(skill.name, amount)


def failed_heal_message(skill):
    return "You use {0} but it fails. ".format(skill.name)


def out_of_punches_message():
    return "You are tired of punching stuff right now. Wait until tomorrow."


def out_of_health_message():
    return get_random_defeat_message()


def battle_message(enemy):
    return "You're punching a {0}.".format(enemy)


def item_dropped(item):
    return "You find {0}.".format(item)


def item_given(npc, item):
    return "{} gives you a {}".format(npc.name, item)


def no_loot(enemy):
    return "You find nothing on the {0}.".format(enemy)


def pixels_dropped_message(pixels):
    return "You gain <span class='pixels'>{} pixels</span>.".format(pixels)


def xp_gained_message(gained_xp):
    return "You gain <span class='xp'>{0}XP!</span>".format(gained_xp)


def bonus_xp_gained_message(reason, bonus_xp):
    return "<span class='xp'>{} Bonus {}XP!</span>".format(reason, bonus_xp)


def run_away_message(enemy_name):
    return "You don't want to punch a stupid {0}.".format(enemy_name)


def begin_combat_sequence(enemy):
    msg = GameMessageManager()
    msg.add("[INITIATING ENVIRONMENT SCAN]", 200)
    msg.add("WARNING: {} {} detected!".format(str(random.choice(DANGER_WORDS)).title(), enemy.enemy_type.name))

    return msg.to_string()


def system_boot():
    msg = GameMessageManager()
    msg.add("Loading BIOS")
    msg.add("Scanning memory", 550)
    msg.add("Checking VRAM", 200)
    msg.add("SYSTEM STATUS: OK")

    return msg.to_string()


def npc_says(npc, message):
    return '{} says "{}"'.format(npc.name, message)


def location_unlocked_message(location_name):
    return "You have unlocked <span class='unlock'>{}</span>.".format(location_name)


def item_added_to_collection(item_type, collection):
    return "You add the {} to your {} collection.".format(item_type.name, collection.name)


