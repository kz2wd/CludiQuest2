class Enemy:
    def __init__(self, name, hp, resistances, physic_damage, magic_damage, elements, armor_piercing):
        self.name = name
        self.hp = hp
        self.hp_max = hp
        self.shield = 0
        self.shield_max = round((hp / 4) + 1, 0)
        self.resistances = resistances
        self.physic_damage = physic_damage
        self.magic_damage = magic_damage
        self.elements = elements
        self.level = 0
        self.experience = 0
        self.inventory = []
        self.items_hold = []
        self.armor_piercing = armor_piercing
        self.dot_dmg = [[]]
        self.dot_heal = [[]]
        self.precision = 1
        self.dodge = 1
        self.alive = True


class EnemyHandler:
    def __init__(self):
        self.enemies = []

    def generate_enemy(self, strength, biome=0):
        self.enemies.append(Enemy("Dummy", 10 * strength, [1, 1, 1, 1, 1, 1], strength, strength,
                                  [strength, strength, strength, strength], 0))

