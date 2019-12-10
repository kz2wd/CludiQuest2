import discord
from GameCore import game


cludigame = game.Game()


class Bot(discord.Client):
    async def on_ready(self):
        print("{}, {}, is ready".format(self.user.name, self.user.id))
        await self.change_presence(activity=discord.Game(name='!!start'))

    async def on_message(self, message):
        if message.author != self.user:
            await cludigame.game_on_message(message)

    async def on_reaction_add(self, reaction, user):
        if user != self.user:
            await cludigame.game_on_reaction(reaction, user)

    async def on_reaction_remove(self, reaction, user):
        if user != self.user:
            await cludigame.game_on_reaction_remove(reaction, user)

