from discord.ext import commands
from trivia import trivia_questions
from trivia.trivia_manager import TriviaManager


class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.channel)
    @commands.command(aliases=["play"], description="Movie trivia. React to the option you think is "
                                                    "correct and gain experience if you're right!")
    async def trivia(self, ctx):
        print("Question raised in channel ID:" + str(ctx.channel.id))
        TriviaManager.clear_trivia_game(str(ctx.channel.id))
        await trivia_questions.ask_random_question(ctx)


def setup(client):
    client.add_cog(Trivia(client))
