import discord
from imdb_manager import IMDbMovieData, IMDbActorData
import glob
import os
import json


class UserData:
    user_dir = "./users"

    is_premium = False
    max_watchlist_size = 50 if is_premium else 10

    default_json_obj = {
            "Watchlist": [{

            }],
            "UserData": [{

            }]
        }

    @classmethod
    def user_save_exists(cls, username):
        for filename in glob.iglob(f"{UserData.user_dir}/*", recursive=True):
            if username in filename:
                return True
        return False

    @classmethod
    async def create_user_save(cls, username):
        with open(os.path.join(UserData.user_dir, f"{username}.json"), "w") as db_file:
            json.dump(UserData.default_json_obj, db_file, ensure_ascii=False, indent=4)

    @classmethod
    async def add_to_save(cls, username, data):
        if not UserData.user_save_exists(username):
            await UserData.create_user_save(str(username))

        with open(os.path.join(UserData.user_dir, f"{username}.json"), "w") as db_file:
            json.dump(data, db_file, ensure_ascii=False, indent=4)


class GlobalDiscordMethods:
    latest_movie_query = None

    @classmethod
    async def display_actor_in_chat(cls, name, ctx):
        actor = IMDbActorData(name)

        embedded_msg = discord.Embed(title=str(actor.actor_obj), description="%s" % str(actor.biography),
                                     color=0x00ff00)
        embedded_msg.set_thumbnail(url=actor.thumbnail)
        embedded_msg.set_image(url=actor.cover)

        await ctx.send(embed=embedded_msg)

    @classmethod
    async def display_movie_in_chat(cls, title, ctx):
        imdb = IMDbMovieData(title)
        GlobalDiscordMethods.latest_movie_query = imdb
        print("latest_movie_query set: " + GlobalDiscordMethods.latest_movie_query.title)

        embedded_msg = discord.Embed(title=imdb.title, description=imdb.plot, color=0x00ff00)
        embedded_msg.set_thumbnail(url=imdb.image)
        embedded_msg.add_field(name="Director", value=imdb.director, inline=False)
        embedded_msg.add_field(name="Cast", value=imdb.stars, inline=False)
        embedded_msg.add_field(name="Genres", value=imdb.genre, inline=False)
        embedded_msg.add_field(name="IMDb rating", value=imdb.rating, inline=False)
        embedded_msg.add_field(name="IMDb link", value=imdb.url, inline=False)
        embedded_msg.add_field(name="Release year", value=imdb.year, inline=False)
        embedded_msg.add_field(name="Runtime", value=imdb.runtime, inline=False)

        embedded_msg.set_footer(text="Want to add this title to your watchlist? Type '!temflix save'")

        await ctx.send(embed=embedded_msg)
