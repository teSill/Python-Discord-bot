import os
import discord
import textwrap
from temflix import Movie
from imdb_manager import IMDbData

TOKEN = os.environ.get('DISCORD_TOKEN')
prefix = "!temflix"

class DiscordClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        if (message.author == self.user):
            return

        message.content = message.content.lower()

        if (message.content.startswith("%s search" % prefix)):
            movie_title = (message.content.split(" search"))[1]
            await message.channel.send("Just a sec, looking up '%s'..." % movie_title)

            try:
                imdb = IMDbData(movie_title);
            except:
                await message.channel.send("Sorry, I couldn't find a movie with that query!")
                return
            
            movie = Movie(imdb.title, imdb.director, imdb.stars, imdb.plot, imdb.genre, imdb.rating, imdb.url, imdb.year, imdb.runtime)

            temflix_result_msg = textwrap.dedent("""\
                Title: %s
                Director: %s
                Stars: %s
                Plot: %s
                Genres: %s
                Rating: %s
                Link: %s
                Release year: %s
                Runtime: %s
                On Netflix: %s

                """ % (movie.title, movie.director, movie.stars, movie.plot, movie.genre, movie.imdb_rating, movie.imdb_link, movie.year, movie.runtime, "maybe but tbh idk"))
            await message.channel.send(temflix_result_msg)
            
        

client = DiscordClient()
client.run(TOKEN)
