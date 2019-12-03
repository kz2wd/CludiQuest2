from Modules import menu


class Fight:
    def __init__(self, players, channel, biome):
        self.players = players
        self.players_id = [player.id for player in self.players]
        self.channel = channel
        self.enemies = None
        self.biome = biome

        self.state = 0
        self.menu_handler = menu.MenuHandler()
        self.action_emote = ['⚔', '🛡', '❤', '✨']
        self.element_emote = ['💧', '🔥', '🌪', '⛰']
        self.target_emote = ['🇦', '🇧', '🇨', '🇩']

    def player_round(self):

        for counter, player in enumerate(self.players):
            pass

    def attack(self, player):
        if player.kit.name == "kit1":

            pass

        else:
            pass
            attack = player.kit.physic_damage + player.kit.elements[0]

    async def display_action(self):
        self.menu_handler.menu_list.append(menu.SimpleMenu(self.action_emote, self.players_id, self.channel,
                                                           sentence="Action"))
        self.menu_handler.menu_list.append(menu.SimpleMenu(self.element_emote, self.players_id, self.channel,
                                                           sentence="Element"))
        self.menu_handler.menu_list.append(menu.SimpleMenu(self.target_emote, self.players_id, self.channel,
                                                           sentence="Cible"))

        await self.menu_handler.menu_list[0].display()
        await self.menu_handler.menu_list[1].display()
        await self.menu_handler.menu_list[2].display()



