from discord.ext import commands
from globals import GlobalDiscordMethods
import json
from user_data import UserData, user_dir


async def add_to_watchlist(ctx, movie_obj):
    username = str(ctx.author)
    user = UserData.get_new_user_instance_by_name(username)

    with open(f"{user_dir}/{username}.json", "r+") as f:
        data = json.load(f)
        watchlist = data["Watchlist"][0]

        if any(movie_obj.title in title for title in watchlist):
            return

        if len(watchlist) == user.max_watchlist_size:
            msg = "Your watchlist is full! Try deleting some entries with '!temflix delete title'." if user.is_premium else \
                "Your watchlist is full! Premium members can hold 5 times as many titles."
            await ctx.send(msg)
            return

        watchlist.update({
            movie_obj.title: movie_obj.url
        })

        await user.add_to_save(data)
        await ctx.message.add_reaction("👍")


class Save(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def save(self, ctx):
        if GlobalDiscordMethods.latest_movie_query is None:
            await ctx.send("Search for a movie first! This command saves the last queried movie.")
            return

        await add_to_watchlist(ctx, GlobalDiscordMethods.latest_movie_query)


def setup(client):
    client.add_cog(Save(client))
