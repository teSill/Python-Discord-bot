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

        print(message.content)

        if (message.content.startswith("%s dog" % prefix)):
            await message.channel.send("no u")

        if (message.content.startswith("%s search" % prefix)):
            movie_title = (message.content.split(" search"))[1]
            await message.channel.send("Just a sec, looking up '%s'..." % movie_title)
            imdb = IMDbData(movie_title);
            movie = Movie(imdb.title, imdb.director, imdb.stars, imdb.plot, imdb.genre, imdb.rating, imdb.url, imdb.year, imdb.runtime, Movie.is_title_on_netflix)

            msg = textwrap.dedent("""\
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

                """ % (movie.title, movie.director, movie.stars, movie.plot, movie.genre, movie.imdb_rating, movie.imdb_link, movie.year, movie.runtime, movie.is_on_netflix))
            #temflix_message = ("""I found %s with your search. Here's some handy info on it!
                                  #Director: %s """ % movie.title, movie.director)
            await message.channel.send(msg)
            


client = DiscordClient()
client.run(TOKEN)
