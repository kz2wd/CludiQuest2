from Modules import menu, ext_utilities as uti
from GameCore import enemies
import discord
import datetime
import random


class Fight:
    def __init__(self, players, channel, biome):
        self.players = players
        self.players_id = [player.discord_info.id for player in self.players]
        self.channel = channel
        self.biome = biome

        self.turn = 0
        self.state = 0
        """0 = playing
        1 = game win
        2 = game lose"""
        self.menu_handler = menu.SimpleMenuHandler()
        self.action_emote = ['⚔', '✨', '🛡', '❤']
        self.element_emote = ['💧', '🔥', '🌪', '⛰']
        self.target_emote = ['🇦', '🇧', '🇨', '🇩']

        self.enemies_handler = enemies.EnemyHandler()
        self.enemies_handler.generate_enemy(1)

        self.effect_player_team = []
        self.effect_enemy_team = []

    async def play_round(self):
        if self.state == 0:
            self.check_death()
            self.check_victory()
            self.players_round()
            self.enemies_round()
            self.menu_handler.__init__()
            await self.display_fight()
            self.turn += 1

        elif self.state == 1:
            await self.channel.send("Vous avez gagné")
        elif self.state == 2:
            await self.channel.send("Vous avez perdu")



    def players_round(self):

        for counter, player in enumerate(self.players):
            player.action = self.menu_handler.menu_list[0].result_list[counter][1]
            player.element = self.menu_handler.menu_list[1].result_list[counter][1]
            player.target = self.menu_handler.menu_list[2].result_list[counter][1]

            if player.action == 0:
                self.direct_attack(player)
            elif player.action == 1:
                self.magic_attack(player)
            elif player.action == 2:
                self.protect(player)
            elif player.action == 3:
                self.heal(player)

        self.effect_applier(self.effect_enemy_team, self.enemies_handler.enemies)

    def direct_attack(self, player):
        if player.target < len(self.enemies_handler.enemies):
            enemy = self.enemies_handler.enemies[player.target]

            resistance = enemy.resistances[4] * player.kit.armor_encountering - player.kit.armor_encountering + 1

            attack = player.kit.physic_damage * 1 / resistance \
                     + player.kit.elements[player.element] * 1 / enemy.resistances[player.element]

            enemy.hp -= attack

    def magic_attack(self, player):
        if player.target < len(self.enemies_handler.enemies):
            if player.kit.name == "Mage":
                enemy = self.enemies_handler.enemies[player.target]

                reduced_magic_damage = uti.divide_to_superior(player.kit.magic_damage, 2)

                mage_enemies = [enemy]
                for i in range(len(self.enemies_handler.enemies) - 1):
                    mage_enemies.append(uti.cycle(player.target, len(self.enemies_handler.enemies)))

                self.effect_enemy_team.append(
                    Effect("magic_damage", reduced_magic_damage, player.element, 1, mage_enemies))

            else:
                enemy = self.enemies_handler.enemies[player.target]

                attack = player.kit.physic_damage * 1 / enemy.resistances[4] + player.kit.elements[player.element] * 1 / \
                         enemy.resistances[player.element]

                enemy.hp -= attack

    def protect(self, player):
        if player.target < len(self.players):
            ally = self.players[player.target]

            if ally.kit.alive:

                if player.kit.name == "Paladin":
                    player.kit.shield = player.kit.shield_max
                    ally.kit.shield = ally.kit.shield_max

                    ally.kit.damage_redirection = player
                else:

                    ally.kit.damage_redirection = player

    def heal(self, player):
        if player.target < len(self.players):
            ally = self.players[player.target]

            if ally.kit.alive:

                heal = player.kit.magic_damage + player.kit.elements[player.element]

                if heal + ally.kit.hp > ally.kit.hp_max:
                    ally.kit.hp = ally.kit.hp_max
                    heal -= (ally.kit.hp_max - ally.kit.hp)

                    if heal + ally.kit.shield > ally.kit.shield_max:
                        ally.kit.shield = ally.kit.shield_max
                    else:
                        ally.kit.shield += heal

                else:
                    ally.kit.hp += heal

    def enemies_round(self):
        for enemy in self.enemies_handler.enemies:
            attack = enemy.physic_damage
            target = random.choice(self.players)

            if target.kit.shield - attack > -1:
                target.kit.shield -= attack
            else:
                attack -= target.kit.shield
                target.kit.shield = 0
                target.kit.hp -= attack

    def check_death(self):
        for player in self.players:
            if player.kit.hp < 1:
                player.kit.alive = False

        for enemy in self.enemies_handler.enemies:
            if enemy.hp < 1:
                self.enemies_handler.enemies.remove(enemy)

    def check_victory(self):
        if len(self.enemies_handler.enemies) == 0:
            self.state = 1

        check = True
        for player in self.players:
            if player.kit.alive:
                check = False
        if check:
            self.state = 2


    async def display_fight(self):
        fight_embed = FightEmbed(self.players, self.enemies_handler.enemies)
        await self.channel.send(content=None, embed=fight_embed.player_embed)
        await self.channel.send(content=None, embed=fight_embed.enemy_embed)

        self.menu_handler.add_simple_menu(menu.SimpleMenu(self.action_emote, self.players_id, self.channel,
                                                          sentence="```Action```"))
        self.menu_handler.add_simple_menu(menu.SimpleMenu(self.element_emote, self.players_id, self.channel,
                                                          sentence="```Element```"))
        self.menu_handler.add_simple_menu(menu.SimpleMenu(self.target_emote, self.players_id, self.channel,
                                                          sentence="```Cible```"))

        await self.menu_handler.menu_list[0].display()
        await self.menu_handler.menu_list[1].display()
        await self.menu_handler.menu_list[2].display()

    def effect_applier(self, effects, team):
        for effect in effects:
            if effect.turn > 0:
                effect.turn -= 1
                if effect.effect_type == "physic_damage":
                    if effect.targets is None:
                        for entity in team:
                            entity.hp -= effect.amount
                    else:
                        for entity in effect.targets:
                            entity.hp -= effect.amount

                elif effect.effect_type == "magic_damage":
                    if effect.targets is None:
                        for entity in team:
                            entity.hp -= effect.amount
                    else:
                        for entity in effect.targets:
                            entity.hp -= effect.amount * 1 / entity.resistance
            else:
                effects.remove(effect)



class Effect:
    def __init__(self, effect_type, amount, element, turn, targets):
        self.effect_type = effect_type
        self.amount = amount
        self.element = element
        self.turn = turn
        self.targets = targets


class FightEmbed:
    def __init__(self, players, enemies, color=0x008000):
        self.player_embed = discord.Embed(description="Etat du groupe", color=color,
                                          timestamp=datetime.datetime.utcnow())
        for player in players:
            self.player_embed.add_field(name=player.discord_info.name,
                                        value="{}, {}".format(player.kit.name, player.kit.level), inline=True)
            self.player_embed.add_field(name="❤️", value="{} /{}".format(int(player.kit.hp), player.kit.hp_max),
                                        inline=True)
            self.player_embed.add_field(name="🛡️", value="{} /{}".format(int(player.kit.shield), player.kit.shield_max),
                                        inline=True)

        self.enemy_embed = discord.Embed(description="Etat des ennemis", color=color,
                                           timestamp=datetime.datetime.utcnow())

        for enemy in enemies:
            self.enemy_embed.add_field(name=enemy.name, value="lvl : {}".format(enemy.level), inline=True)
            self.enemy_embed.add_field(name="❤️", value="{} /{}".format(int(enemy.hp), enemy.hp_max), inline=True)
            self.enemy_embed.add_field(name="🛡️", value="{} /{}".format(int(enemy.shield), enemy.shield_max),
                                       inline=True)





