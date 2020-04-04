import os
import discord
import textwrap
from temflix import Movie
from imdb_manager import IMDbData
from tmdb_manager import TMDB

TOKEN = os.environ.get('DISCORD_TOKEN')
prefix = "!temflix"

class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has gone online!')

    async def on_message(self, message):
        if (message.author == self.user):
            return

        message.content = message.content.lower()

        if message.content.startswith("%s search" % prefix):
            movie_title = (message.content.split(" search"))[1]
            await message.channel.send("Just a sec, looking up '%s'..." % movie_title)

            try:
                imdb = IMDbData(movie_title);
            except:
                await message.channel.send("Sorry, I couldn't find a movie with that query!")
                return
            
            movie = Movie(imdb.title, imdb.director, imdb.stars, imdb.plot, imdb.genre, imdb.rating, imdb.url, imdb.year, imdb.runtime, imdb.image)

            embedded_msg = discord.Embed(title=movie.title, description=movie.plot, color=0x00ff00)
            embedded_msg.set_thumbnail(url=movie.image)
            embedded_msg.add_field(name="Director", value=movie.director, inline=False)
            embedded_msg.add_field(name="Cast", value=movie.stars, inline=False)
            embedded_msg.add_field(name="Genres", value=movie.genre, inline=False)
            embedded_msg.add_field(name="IMDb rating", value=movie.imdb_rating, inline=False)
            embedded_msg.add_field(name="IMDb link", value=movie.imdb_link, inline=False)
            embedded_msg.add_field(name="Release year", value=movie.year, inline=False)
            embedded_msg.add_field(name="Runtime", value=movie.runtime, inline=False)
            
            await message.channel.send(embed = embedded_msg)

        if message.content.startswith("%s help" % prefix) or message.content.startswith("%s commands" % prefix):
            embedded_msg = discord.Embed(title="Help", description="temflix is a bot with deep interest and knowledge in the entertainment industry! Here's a list of its current commands:", color=0x00ff00)
            embedded_msg.add_field(name="'!temflix help' or '!temflix commands'", value="Opens up this panel.", inline=False)
            embedded_msg.add_field(name="'!temlix search movie''", value="eg. '!temflix search goodfellas'. This will return a set of handy info about the movie.", inline=False)
            embedded_msg.add_field(name="'!temflix popular'", value="Displays 20 of the currently most popular movies.", inline=False)

            await message.channel.send(embed = embedded_msg)

        if message.content.startswith("%s popular" % prefix):
            popular_movies = TMDB.get_popular_movies()

            embedded_msg = discord.Embed(title="Popular movies", description="20 currently popular movies. This list changes daily!", color=0x00ff00)
            for index, pop in enumerate(popular_movies, start=1):
                embedded_msg.add_field(name='%s.'% index, value=pop.title, inline=True)

            await message.channel.send(embed = embedded_msg)
            
client = DiscordClient()
client.run(TOKEN)
