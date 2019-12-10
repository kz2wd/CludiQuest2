from Modules import menu, ext_utilities as utilities
from Displays import emotes, my_menus, messages as msg
from GameCore import all_kit, fight, player as player_class
from Lore import biomes


class Game:
    def __init__(self):
        self.players = []
        self.players_id = []
        self.game_players = []
        self.state = 0
        """
        0 = not initialized
        1 = waiting for chef to choose type of game
        2 = waiting for players
        3 = choosing kit
        4 = choosing area
        5 = fighting
        """
        self.channel = None
        self.menus_handler = menu.MenuHandler()
        self.game_type = None
        self.kit_handler = all_kit.KitHandler()
        self.biomes = []
        self.biome = None
        self.fight = None

    async def game_on_message(self, message):
        if self.state == 0:
            if message.content == "!quest":
                await self.start(message)

    async def game_on_reaction(self, reaction, user):
        self.menus_handler.on_reaction_add_menu(reaction, user)
        if self.state == 1:
            if user.id == self.players[0].id:
                self.set_game_type(self.menus_handler.menu_list[0].result_list[0][1])
                await self.invite_player()

        if self.state == 2:
            await self.add_player(reaction, user)

        if utilities.check_presence(user.id, self.players_id):
            if self.state == 3:
                await self.set_kit()

            elif self.state == 4:
                await self.set_biome()

            elif self.state == 5:
                self.fight.menu_handler.on_reaction_add_menu(reaction, user)
                await self.play_fight()

    async def game_on_reaction_remove(self, reaction, user):
        self.menus_handler.on_reaction_remove_menu(reaction, user)
        if self.state == 5:
            self.fight.menu_handler.on_reaction_remove_menu(reaction, user)

    async def start(self, message):
        self.players = [message.author]
        self.channel = message.channel
        self.state = 1
        print("state 1")

        self.menus_handler.menu_list = [my_menus.choose_game_mode([message.author.id], self.channel)]

        await self.menus_handler.menu_list[0].display()

    async def add_player(self, reaction, user):
        if reaction.emoji == emotes.join_game:
            if len(self.players) < 5:

                if not utilities.check_presence(user, self.players):

                        self.players.append(user)

                        await self.channel.send("{}, aussi connu comme {}, a rejoint la partie !   {} / 4"
                                                .format(user.name, user.nick, len(self.players)))
            if user == self.players[0]:
                await self.channel.send(msg.start_game)
                self.state = 3
                print("state 3")
                self.players_id = [player.id for player in self.players]

                self.menus_handler.menu_list = [my_menus.choose_kit(self.players_id, self.channel)]
                await self.menus_handler.menu_list[0].display()

    def set_game_type(self, mode_choose):
        if -1 < mode_choose < 3:  # for now, there is 0, 1 or 2
            self.game_type = mode_choose
        else:
            print("WARNING! GAME MODE ERROR")

        self.state = 2
        print("state 2")

    async def invite_player(self):
        message = await self.channel.send(msg.join_game)
        await message.add_reaction(emotes.join_game)

    async def game_type_0(self):
        pass

    async def set_kit(self):
        if self.menus_handler.menu_list[0].menu_is_answered():
            for i in range(len(self.players)):
                kit = self.kit_handler.give_kit(self.menus_handler.menu_list[0].result_list[i][1])

                self.game_players.append(player_class.Player(self.players[i], kit))
                print("{} a choisi la classe {}".format(self.players[i].name, kit.name))
            self.state = 4
            print("state 4")

            self.menus_handler.menu_list = [my_menus.choose_start_biome([self.players[0].id], self.channel)]
            await self.menus_handler.menu_list[0].display()

    async def set_biome(self):
        if self.menus_handler.menu_list[0].menu_is_answered():
            self.biomes.append(biomes.start_zones[self.menus_handler.menu_list[0].result_list[0][1]])
            self.biome = self.biomes[-1]
            print(self.biomes)
            self.state = 5
            print("state 5")
            await self.start_fight()

    async def start_fight(self):
        self.fight = fight.Fight(self.game_players, self.channel, self.biome)
        await self.fight.display_fight()

    async def play_fight(self):
        if self.fight.menu_handler.menu_list[0].menu_is_answered():
            if self.fight.menu_handler.menu_list[1].menu_is_answered():
                if self.fight.menu_handler.menu_list[2].menu_is_answered():
                    await self.fight.play_round()



