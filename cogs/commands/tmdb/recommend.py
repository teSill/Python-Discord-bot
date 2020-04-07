import discord
from discord.ext import commands
from tmdb_manager import TMDB
from globals import GlobalDiscordMethods
from user_data import UserData
import json


class Recommend(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Recommends you a movie based on your watchlist. You "
                                  "can pass in a number to act as the minimum rating "
                                  "for your query: eg. '!temflix recommend 7.5'",
                      pass_context=True)
    async def recommend(self, ctx, *, user_input="6.5"):
        user = UserData(str(ctx.author))
        with open(user.get_full_path_for_edit(), "r+") as f:
            data = json.load(f)
            if len(list(data["Watchlist"][0].keys())) == 0:
                await ctx.send("You'll need at least one title in your watchlist to get recommendations.")
                return

        try:
            user_input = float(user_input)
        except ValueError:
            return

        if user_input > 10:
            await ctx.send("Enter a minimum rating between 1 and 10.")
            return

        await ctx.send(f"One moment - finding you a title with a minimum rating of {user_input}.")
        recommended_movie = TMDB.get_recommended_movie(str(ctx.author), user_input)

        if recommended_movie is None:
            await ctx.send("Couldn't find titles up to your standards, sorry.")
            return

        await GlobalDiscordMethods.display_movie_in_chat(recommended_movie.title, ctx)
        # except:
        # print("There was an error retrieving a recommended movie from The Movie Database.")


def setup(client):
    client.add_cog(Recommend(client))
