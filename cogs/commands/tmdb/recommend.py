import discord
from discord.ext import commands
from tmdb_manager import TMDB
from imdb_manager import IMDbMovieData


class Recommend(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Recommends you a movie based on your watchlist.")
    async def recommend(self, ctx):
        #try:
        recommended_movie = TMDB.get_recommended_movie(str(ctx.author))
        if recommended_movie is None:
            await ctx.send("Couldn't find anything other than shit movies, sorry.")
            return

        embedded_msg = discord.Embed(title="Recommended movie",
                                     description=f"Based on your watchlist, I'm recommending you...\n\n"
                                                 f"Title: {recommended_movie.title}\n\n"
                                                 f"Plot: {recommended_movie.overview}\n\n"
                                                 f"Rating: {recommended_movie.vote_average}\n",
                                     color=0x00ff00)

        cover_url = IMDbMovieData.get_cover_image_url(recommended_movie.title)
        embedded_msg.set_thumbnail(url=cover_url)
        embedded_msg.set_image(url=cover_url)

        await ctx.send(embed=embedded_msg)
        #except:
            #print("There was an error retrieving a recommended movie from The Movie Database.")


def setup(client):
    client.add_cog(Recommend(client))
