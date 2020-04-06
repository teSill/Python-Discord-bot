from discord.ext import commands
from globals import GlobalDiscordMethods, UserData
import json
import glob


async def add_to_watchlist(ctx, movie_obj):
    if not UserData.user_save_exists(str(ctx.author)):
        await UserData.create_user_save(str(ctx.author))

    with open(f"{UserData.user_dir}/{str(ctx.author)}.json", "r+") as f:
        data = json.load(f)
        watchlist = data["Watchlist"][0]

        if any(movie_obj.title in title for title in watchlist):
            return

        if len(watchlist) == UserData.max_watchlist_size:
            msg = "Your watchlist is full! Try deleting some entries with '!temflix delete title'." if UserData.is_premium else \
                "Your watchlist is full! Premium members can hold 5 times as many titles."
            await ctx.send(msg)
            return

        watchlist.update({
            movie_obj.title: movie_obj.url
        })

        await UserData.add_to_save(str(ctx.author), data)
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
