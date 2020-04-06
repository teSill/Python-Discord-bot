import os
import discord
from discord.ext import commands
from temflix import Movie
from imdb_manager import IMDbMovieData, IMDbActorData
from tmdb_manager import TMDB

TOKEN = os.environ.get('DISCORD_TOKEN')
custom_commands = ["find", "commands", "popular", "findactor", "findactress", "findmovie"]

client = commands.Bot(command_prefix='!temflix ')


async def display_actor(name, ctx):
    actor = IMDbActorData(name)

    embedded_msg = discord.Embed(title=str(actor.actor_obj), description="%s" % str(actor.biography),
                                 color=0x00ff00)
    embedded_msg.set_thumbnail(url=actor.thumbnail)
    embedded_msg.set_image(url=actor.cover)

    await ctx.send(embed=embedded_msg)


async def display_movie(title, ctx):
    imdb = IMDbMovieData(title);
    movie = Movie(imdb.title, imdb.director, imdb.stars, imdb.plot, imdb.genre, imdb.rating, imdb.url, imdb.year,
                  imdb.runtime, imdb.image)
    print(movie.title)

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


@client.event
async def on_ready():
    print("Temflix has come online!")


@client.command(pass_context=True)
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(pass_context=True, help="Finds a movie or actor/actress with your command. Movies are prioritized.")
async def find(ctx, *, user_input):
    await ctx.channel.send("Looking up '%s' - just a second!" % user_input)
    try:
        await display_movie(user_input, ctx)
    except:
        print("Couldn't find a movie with given query. Trying to find an actor with it...")
        try:
            await display_actor(user_input, ctx)
        except:
            print("Couldn't find an actor either")
            await ctx.channel.send("Sorry, I couldn't find a result with that query!")
        return


@client.command(name="findmovie", pass_context=True)
async def find_movie(ctx, *, user_input):
    await ctx.send("Looking up '%s' - just a second!" % user_input)
    try:
        await display_movie(user_input, ctx)
    except:
        await ctx.send("Sorry, I couldn't find a movie with that query!")


@client.command(aliases=["findactor", "findactress"], pass_context=True)
async def find_actor(ctx, *, user_input):
    await ctx.send("Looking up '%s' - just a second!" % user_input)
    try:
        await display_actor(user_input, ctx)
    except:
        await ctx.channel.send(
            "Sorry, I couldn't find an actor/actress with that query! They probably aren't registered on IMDb or have an incomplete profile.")


@client.command(pass_context=True)
async def popular(ctx):
    popular_movies = TMDB.get_popular_movies()

    embedded_msg = discord.Embed(title="Popular movies",
                                 description="10 currently popular movies in The Movie Database (TMDb). This list changes daily!",
                                 color=0x00ff00)
    for index, pop in enumerate(popular_movies, start=1):
        embedded_msg.add_field(name='%s.' % index, value=pop.title + "\nAverage rating: " + str(pop.vote_average),
                               inline=False)

    await ctx.send(embed=embedded_msg)


@client.command(pass_context=True)
async def commands(ctx):
    embedded_msg = discord.Embed(title="Help",
                                 description="temflix is a bot with deep interest and knowledge in the entertainment industry! Here's a list of its current commands:",
                                 color=0x00ff00)
    embedded_msg.add_field(name="'!temflix help' or '!temflix commands'", value="Opens up this panel.",
                           inline=False)
    embedded_msg.add_field(name="'!temlix movie' and '!temlix actor'",
                           value="eg. '!temflix goodfellas'. Search for a movie or an actor/actress. Movies are prioritized with this query.",
                           inline=False)
    embedded_msg.add_field(name="'!temlix find movie' and '!temlix find actor'",
                           value="eg. '!temflix find rami malek'. Performs a more detailed search than the above command.",
                           inline=False)
    embedded_msg.add_field(name="'!temflix popular'", value="Displays 10 of the currently most popular movies.",
                           inline=False)

    await ctx.send(embed=embedded_msg)


@client.command(pass_context=True)
async def on_message(self, message):
    if message.author == self.user:
        return

    message.content = message.content.lower()


client.run(TOKEN)
