from discord.ext import commands
import random
from trivia_manager import TriviaManager


class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["play"], description="Movie trivia.")
    async def trivia(self, ctx):
        responses = {"Which movie won best picture in 2011?": "The Artist",
                     "Which movie won best picture in 2000?": "Gladiator",
                     "Which movie won best picture in 2017?": "The Shape of Water",
                     "Which movie won best picture in 1995?": "Braveheart",
                     }

        print("Question raised in channel ID:" + str(ctx.channel.id))
        key, val = random.choice(list(responses.items()))

        await ctx.send(key)
        await TriviaManager.create_trivia_game(str(ctx.channel.id), val)


def setup(client):
    client.add_cog(Trivia(client))
