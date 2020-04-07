import discord
from discord.ext import commands
import random


class EightBall(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["8ball"], description="Have the magic 8ball answer your most burning questions.")
    async def eight_ball(self, ctx):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "I'm the most certain I've ever been that the answer is yes.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Absolutely maybe.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good",
                     "Very doubtful",
                     "Certainly not.",
                     "How could you even suggest otherwise?"
                     "I'm the most certain I've ever been that the answer is no.",
                     ]
        await ctx.send(random.choice(responses))


def setup(client):
    client.add_cog(EightBall(client))
