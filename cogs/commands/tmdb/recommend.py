import discord
from discord.ext import commands
from tmdb_manager import TMDB
from imdb_manager import IMDbMovieData


class Recommend(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["recommendminrate"], description="Recommends you a movie based on your watchlist.", pass_context=True)
    async def recommend(self, ctx, *, user_input="6.5"):

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

        embedded_msg = discord.Embed(title=f"Recommended title: {recommended_movie.title}",
                                     description=f"\n\nPlot: \n\n{recommended_movie.overview}\n\n"
                                                 f"TMDb rating: \n\n{recommended_movie.vote_average}\n",
                                     color=0x00ff00)

        cover_url = IMDbMovieData.get_cover_image_url(recommended_movie.title)
        embedded_msg.set_thumbnail(url=cover_url)
        embedded_msg.set_image(url=cover_url)

        await ctx.send(embed=embedded_msg)
        #except:
            #print("There was an error retrieving a recommended movie from The Movie Database.")


def setup(client):
    client.add_cog(Recommend(client))
