from discord.ext import commands
from user_data import UserData
import json
import discord


class CopyWatchlist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["copy", "copywatchlist"], pass_context=True, description="Copies the watchlist of the "
                                                                                        "given user"
                                                                                        "and makes it your own!")
    async def copy_watchlist(self, ctx, *, user_input):
        username = str(ctx.author)
        user = UserData.create_user_instance_by_name(username)
        other_user = UserData.create_user_instance_by_name(user_input)

        if username == user_input:
            return

        with open(other_user.get_full_path_for_edit(), "r+") as f:
            data = json.load(f)
            watchlist = data["Watchlist"][0]

            if len(watchlist) == 0:
                await ctx.channel.send(f"{other_user.username} doesn't have a watchlist! Be sure to enter their name "
                                       f"correctly along with their # ID.")
                return

            new_watchlist = watchlist

        with open(user.get_full_path_for_edit(), "r+") as f:
            data = json.load(f)
            data["Watchlist"][0] = new_watchlist

            await user.update_watchlist(data)
            await ctx.message.add_reaction("👍")


def setup(client):
    client.add_cog(CopyWatchlist(client))
