import os
import discord
import textwrap
from temflix import Movie
from imdb_manager import IMDbMovieData, IMDbActorData
from tmdb_manager import TMDB
import tasks

TOKEN = os.environ.get('DISCORD_TOKEN')
prefix = "!temflix"
commands = ["find", "search", "help", "commands", "popular", "find actor", "find movie"]

class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has come online!')

    async def on_message(self, message):
        if (message.author == self.user):
            return

        async def find_actor(name, message):
            actor = IMDbActorData(name)

            embedded_msg = discord.Embed(title=str(actor.actor_obj), description="%s" % str(actor.biography), color=0x00ff00)
            embedded_msg.set_thumbnail(url=actor.thumbnail)
            embedded_msg.set_image(url=actor.cover)

            await message.channel.send(embed = embedded_msg)

        async def find_movie(title, message):
            imdb = IMDbMovieData(title);
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

        message.content = message.content.lower()

        if message.content.startswith("%s " % prefix) and message.content.split()[1] not in commands:
            title = message.content.split("%s " % prefix)[1]
            await message.channel.send("Looking up '%s' - just a second!" % title)

            try:
                await find_movie(title, message)
            except:
                print("Couldn't find a movie with given query. Trying to find an actor with it...")
                try:
                    await find_actor(title, message)
                except:
                    print("Couldn't find an actor either")
                    await message.channel.send("Sorry, I couldn't find a result with that query!")
                return

        if message.content.startswith("%s find movie" % prefix):
            title = message.content.split("movie ")[1]
            await message.channel.send("Looking up '%s' - just a second!" % title)
            try:
                await find_movie(title, message)
            except:
                await message.channel.send("Sorry, I couldn't find a movie with that query!")
                
        if message.content.startswith("%s find actor" % prefix) or message.content.startswith("%s find actress" % prefix):
            actor_name = movie_title = message.content.split(" actor ")[1] if "actor" in message.content else message.content.split(" actress ")[1]
            
            await message.channel.send("Looking up '%s' - just a second!" % actor_name)
            try:
                await find_actor(actor_name, message)
            except:
                await message.channel.send("Sorry, I couldn't find an actor/actress with that query! They probably aren't registered on IMDb or have an incomplete profile.")
        
        if message.content.startswith("%s help" % prefix) or message.content.startswith("%s commands" % prefix):
            embedded_msg = discord.Embed(title="Help", description="temflix is a bot with deep interest and knowledge in the entertainment industry! Here's a list of its current commands:", color=0x00ff00)
            embedded_msg.add_field(name="'!temflix help' or '!temflix commands'", value="Opens up this panel.", inline=False)
            embedded_msg.add_field(name="'!temlix movie' and '!temlix actor'", value="eg. '!temflix goodfellas'. Search for a movie or an actor/actress. Movies are prioritized with this query.", inline=False)
            embedded_msg.add_field(name="'!temlix find movie' and '!temlix find actor'", value="eg. '!temflix find rami malek'. Performs a more detailed search than the above command.", inline=False)
            embedded_msg.add_field(name="'!temflix popular'", value="Displays 10 of the currently most popular movies.", inline=False)

            await message.channel.send(embed = embedded_msg)

        if message.content.startswith("%s popular" % prefix):
            popular_movies = TMDB.get_popular_movies()

            embedded_msg = discord.Embed(title="Popular movies", description="10 currently popular movies in The Movie Database (TMDb). This list changes daily!", color=0x00ff00)
            for index, pop in enumerate(popular_movies, start=1):
                embedded_msg.add_field(name='%s.'% index, value=pop.title + "\nAverage rating: " + str(pop.vote_average), inline=False)

            await message.channel.send(embed = embedded_msg)

        if message.content == "%s rep" % prefix:
            await message.channel.send("https://support-leagueoflegends.riotgames.com/hc/en-us/articles/360034625773-Report-a-Player-After-a-Game?flash_digest=2a9ac715940d3c51894bd52ba63fd43e65324ab8")

            
client = DiscordClient()
client.run(TOKEN)
