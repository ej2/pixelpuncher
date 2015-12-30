

def low_energy_message(skill):
    return "<span class='hit'>You don't have enough energy to perform {0}!</span>".format(skill.name)


def successful_hit_message(skill, enemy, damage):
    return "<span class='hit'>You {0} the {1} and hit for {2} damage!</span>".format(
        skill.name, enemy, damage)


def successful_critical_message(skill, enemy, damage):
    hit_message = successful_hit_message(skill, enemy, damage)
    return "{0}<span class='critial'>CRITIAL HIT!</span>".format(hit_message)


def hit_failure_message(skill, enemy):
    return "<span class='miss'>You try to {0} the {1} and miss!</span>".format(skill.name, enemy)


def victory_message():
    return "<span class='victory'>Victory!</span>"


def player_damage_message(damage):
    return "You hurt your hand. You lose <span class='health'>{0} health</span>.".format(damage)
