import discord
from discord.ext import commands
from tmdb_manager import TMDB


class Popular(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def popular(self, ctx):
        try:
            popular_movies = TMDB.get_popular_movies()

            embedded_msg = discord.Embed(title="Popular movies",
                                         description="10 currently popular movies in The Movie Database (TMDb). This "
                                                     "list changes daily!",
                                         color=0x00ff00)
            for index, pop in enumerate(popular_movies, start=1):
                embedded_msg.add_field(name='%s.' % index,
                                       value=pop.title + "\nAverage rating: " + str(pop.vote_average),
                                       inline=False)

            await ctx.send(embed=embedded_msg)
        except:
            await ctx.channel.send(
                "There was an error retrieving popular movies from The Movie Database.")


def setup(client):
    client.add_cog(Popular(client))
