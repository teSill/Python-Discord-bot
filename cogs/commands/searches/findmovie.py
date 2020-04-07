import discord
from discord.ext import commands
from globals import GlobalDiscordMethods


class FindMovie(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="findmovie", pass_context=True, description="eg. '!temflix findactor rami malek'. Performs "
                                                                       "a more detailed search than the above "
                                                                       "command.")
    async def find_movie(self, ctx, *, user_input):
        await ctx.send("Looking up '%s' - just a second!" % user_input)
        try:
            await GlobalDiscordMethods.display_movie_in_chat(user_input, ctx)
        except:
            await ctx.send("Sorry, I couldn't find a movie with that query!")


def setup(client):
    client.add_cog(FindMovie(client))