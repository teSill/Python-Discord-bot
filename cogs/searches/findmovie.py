import discord
from discord.ext import commands
from discord_globals import GlobalMethods


class FindMovie(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="findmovie", pass_context=True)
    async def find_movie(self, ctx, *, user_input):
        await ctx.send("Looking up '%s' - just a second!" % user_input)
        try:
            await GlobalMethods.display_movie_in_chat(user_input, ctx)
        except:
            await ctx.send("Sorry, I couldn't find a movie with that query!")


def setup(client):
    client.add_cog(FindMovie(client))