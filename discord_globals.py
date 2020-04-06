import discord
from imdb_manager import IMDbMovieData, IMDbActorData
from temflix import Movie

class GlobalMethods():
    async def display_actor_in_chat(name, ctx):

        actor = IMDbActorData(name)

        embedded_msg = discord.Embed(title=str(actor.actor_obj), description="%s" % str(actor.biography),
                                 color=0x00ff00)
        embedded_msg.set_thumbnail(url=actor.thumbnail)
        embedded_msg.set_image(url=actor.cover)

        await ctx.send(embed=embedded_msg)


    async def display_movie_in_chat(title, ctx):
        imdb = IMDbMovieData(title)
        movie = Movie(imdb.title, imdb.director, imdb.stars, imdb.plot, imdb.genre, imdb.rating, imdb.url, imdb.year,
                      imdb.runtime, imdb.image)

        embedded_msg = discord.Embed(title=movie.title, description=movie.plot, color=0x00ff00)
        embedded_msg.set_thumbnail(url=movie.image)
        embedded_msg.add_field(name="Director", value=movie.director, inline=False)
        embedded_msg.add_field(name="Cast", value=movie.stars, inline=False)
        embedded_msg.add_field(name="Genres", value=movie.genre, inline=False)
        embedded_msg.add_field(name="IMDb rating", value=movie.imdb_rating, inline=False)
        embedded_msg.add_field(name="IMDb link", value=movie.imdb_link, inline=False)
        embedded_msg.add_field(name="Release year", value=movie.year, inline=False)
        embedded_msg.add_field(name="Runtime", value=movie.runtime, inline=False)

        await ctx.send(embed=embedded_msg)