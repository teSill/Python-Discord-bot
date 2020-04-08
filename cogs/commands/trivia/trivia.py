import discord
from discord.ext import commands
import random
from trivia_manager import TriviaManager


class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["play"], description="Movie trivia.")
    async def trivia(self, ctx):
        random_question = TriviaManager.get_random_question()

        question = random_question["question"]
        correct_answer = random_question["correct_answer"]
        answers = random_question["options"]

        embedded_msg = discord.Embed(title=str(question), description="", color=0x00ff00)

        options = {
            "A": answers[0],
            "B": answers[1],
            "C": answers[2],
            "D": answers[3]
        }

        for key, value in options.items():
            if value == random_question["correct_answer"]:
                correct_answer = key.lower()
            embedded_msg.add_field(name='\u200b', value=f"{key}: {value}", inline=False)

        print("Question raised in channel ID:" + str(ctx.channel.id) + ". Correct choice: " + correct_answer)
        await ctx.send(embed=embedded_msg)
        await TriviaManager.create_trivia_game(str(ctx.channel.id), correct_answer)



def setup(client):
    client.add_cog(Trivia(client))
