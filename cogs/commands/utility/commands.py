import discord
from discord.ext import commands


async def display_commands_in_chat(ctx):
    embedded_msg = discord.Embed(title="Help",
                                 description="Temflix is a bot with deep interest and knowledge in the entertainment "
                                             "industry! Here's a list of its current commands:\n",
                                 color=0x00ff00)
    embedded_msg.add_field(name="'!temflix commands' and '!temflix help'", value="Opens up this panel.\n",
                           inline=False)
    embedded_msg.add_field(name="'!temlix find'",
                           value="eg. '!temflix find goodfellas'. Search for a movie or an actor/actress. Movies are "
                                 "prioritized with this query.",
                           inline=False)
    embedded_msg.add_field(name="'!temlix findmovie' and '!temlix findactor'",
                           value="eg. '!temflix findactor rami malek'. Performs a more detailed search than the above "
                                 "command.",
                           inline=False)
    embedded_msg.add_field(name="'!temflix popular'", value="Displays 10 of the currently most popular movies on The "
                                                            "Movie Database (IMDb).\n\n",
                           inline=False)
    embedded_msg.add_field(name="'!temflix save'", value="Saves the last queried movie to your watchlist.",
                           inline=False)
    embedded_msg.add_field(name="'!temflix watchlist'", value="Displays your watchlist.",
                               inline=False)
    embedded_msg.add_field(name="'!temflix copywatchlist user'", value="Copies the watchlist of the user you enter "
                                                                       "and makes it your own!",
                           inline=False)


    await ctx.send(embed=embedded_msg)


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["help"])
    async def commands(self, ctx):
        await display_commands_in_chat(ctx)


def setup(client):
    client.add_cog(Commands(client))
