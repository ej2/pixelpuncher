

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


def player_damage_message(damage):
    return "You hurt your hand. You lose <span class='health'>{0} health</span>. ".format(int(damage))


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
    return "Your hands hurt too much right now to punch stuff. Maybe you should have a refreshing sports drink."
