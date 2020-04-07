import discord
from discord.ext import commands


class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["help"], description="Temflix is a bot with deep interest and knowledge in the "
                                                    "entertainment industry! Here's a list of its current commands:")
    async def commands(self, ctx):
        embedded_msg = discord.Embed(title="Help",
                                     description=f"{Commands.commands.description}\n",
                                     color=0x00ff00)
        embedded_msg.add_field(name="'!temflix commands' and '!temflix help'", value="Opens up this panel.\n",
                               inline=False)
        embedded_msg.add_field(name="'!temlix find'",
                               value=ctx.bot.get_cog("Find").find.description,
                               inline=False)
        embedded_msg.add_field(name="'!temlix findmovie' and '!temlix findactor'",
                               value=ctx.bot.get_cog("FindMovie").find_movie.description,
                               inline=False)
        embedded_msg.add_field(name="'!temflix popular'",
                               value=ctx.bot.get_cog("Popular").popular.description,
                               inline=False)
        embedded_msg.add_field(name="'!temflix save'",
                               value=ctx.bot.get_cog("Save").save.description,
                               inline=False)
        embedded_msg.add_field(name="'!temflix watchlist'",
                               value=ctx.bot.get_cog("Watchlist").watchlist.description,
                               inline=False)
        embedded_msg.add_field(name="'!temflix copy user'",
                               value=ctx.bot.get_cog("CopyWatchlist").copy_watchlist.description,
                               inline=False)
        embedded_msg.add_field(name="'!temflix delete movie'",
                               value=ctx.bot.get_cog("Delete").delete.description,
                               inline=False)
        embedded_msg.add_field(name="'!temflix clear'",
                               value=ctx.bot.get_cog("Clear").clear.description,
                               inline=False)
        embedded_msg.add_field(name="'!temflix recommend' or !temflix recommend n'",
                               value=ctx.bot.get_cog("Recommend").recommend.description,
                               inline=False)
        await ctx.send(embed=embedded_msg)


def setup(client):
    client.add_cog(Commands(client))
