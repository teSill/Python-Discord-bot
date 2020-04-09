from discord.ext import commands
import trivia_questions


class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["play"], description="Movie trivia.")
    async def trivia(self, ctx):
        print("Question raised in channel ID:" + str(ctx.channel.id))
        await ctx.send("Just a moment!")
        await trivia_questions.ask_random_question(ctx)


def setup(client):
    client.add_cog(Trivia(client))
