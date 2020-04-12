from discord.ext import commands
from globals import GlobalDiscordMethods
import json
from user_data import UserData
import imdb_manager


async def add_to_watchlist(ctx, movie_obj):
    username = str(ctx.author)
    user = UserData.create_user_instance_by_name(username)

    with open(user.get_full_path_for_edit(), "r+") as f:
        data = json.load(f)
        watchlist = data["Watchlist"][0]

        if any(movie_obj.title in title for title in watchlist):
            await ctx.message.add_reaction("👎")
            return

        if len(watchlist) == user.max_watchlist_size:
            msg = "Your watchlist is full! Try deleting some entries with '!temflix delete title'." if user.is_premium else \
                "Your watchlist is full! If you'd like to support the developer, please consider purchasing Premium " \
                "and you'll be able to keep over 3 times as many titles in your watchlist too!"
            await ctx.send(msg)
            await ctx.message.add_reaction("👎")
            return

        try:
            watchlist.update({
                movie_obj.title: movie_obj.url
            })
        except AttributeError:
            watchlist.update({
                movie_obj.title: imdb_manager.get_movie_url(movie_obj.title)
            })

        await user.update_watchlist(data)
        await ctx.message.add_reaction("👍")


class Save(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Saves the last queried movie to your watchlist.")
    async def save(self, ctx):
        if GlobalDiscordMethods.latest_movie_query is None:
            await ctx.send("Search for a movie first! This command saves the last queried movie.")
            return

        await add_to_watchlist(ctx, GlobalDiscordMethods.latest_movie_query)


def setup(client):
    client.add_cog(Save(client))
