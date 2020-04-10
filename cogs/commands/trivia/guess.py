from discord.ext import commands
from trivia.trivia_manager import TriviaManager
from user_data import UserData

right_answer_exp = 10


class Guess(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["answer", "reply"], description="Movie trivia.")
    async def guess(self, ctx, *, user_input):
        channel_id = str(ctx.channel.id)
        correct_answer = TriviaManager.get_correct_answer(channel_id)
        if correct_answer is None:
            return

        if correct_answer.lower() == user_input.lower():
            TriviaManager.clear_trivia_game(channel_id)
            user = UserData(str(ctx.author))
            user.add_experience(right_answer_exp)

            await ctx.send(f"That's correct! You received {right_answer_exp} exp -  you now have {user.get_experience()}.")
            return

        print(f"User guessed {user_input.lower()} but the right answer is {correct_answer.lower()}")
        await ctx.send("Try again.")


def setup(client):
    client.add_cog(Guess(client))
