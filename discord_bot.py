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

            embed = discord.Embed(title=movie.title, description=movie.plot, color=0x00ff00)
            embed.add_field(name="Director", value=movie.director, inline=True)
            embed.add_field(name="Cast", value=movie.stars, inline=True)
            embed.add_field(name="Genres", value=movie.genre, inline=True)
            embed.add_field(name="IMDb rating", value=movie.imdb_rating, inline=True)
            embed.add_field(name="IMDb link", value=movie.imdb_link, inline=True)
            embed.add_field(name="Release year", value=movie.year, inline=True)
            embed.add_field(name="Runtime", value=movie.runtime, inline=True)
            
            await message.channel.send(embed = embed)
            
        

client = DiscordClient()
client.run(TOKEN)
