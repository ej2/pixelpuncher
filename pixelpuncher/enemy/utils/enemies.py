
class EnemyBase(object):
    enemy = None  # database record

    def __init__(self, enemy):
        self.enemy = enemy

    def attack(self):
        """

        :return: damage amount
        """
        raise NotImplementedError

    def hit(self, damage, damage_type):
        """
        Called when player successfully hits the enemy
        :param damage:
        :param damage_type: could be used to increase or decrease total damage
        :return:
        """
        self.enemy.adjust_health(damage)

    @property
    def can_attack(self):
        pass

    @property
    def is_defeated(self):
        pass

    def calculate_xp(self):
        return self.enemy.enemy_type.xp

    def save(self):
        self.enemy.save()

