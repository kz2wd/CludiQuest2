class Kit:
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


class KitHandler:
    def __init__(self):
        self.kits = [Kit("Chevalier", 12, [1.2, 1.2, 1.2, 1.2, 1, 1], 3, 1, [2, 2, 2, 2], 0),
                     Kit("Paladin", 17, [1, 1, 1, 1, 1.5, 1.5], 3, 3, [0, 0, 0, 0], 0),
                     Kit("Mage", 10, [1, 1, 1, 1, 1, 1], 2, 5, [0, 0, 0, 0], 0),
                     Kit("Archer", 7, [1, 1, 1, 1, 1], 7, 1, [0, 0, 0, 0], 0)]

    def give_kit(self, kit_id):
        return self.kits[kit_id]






