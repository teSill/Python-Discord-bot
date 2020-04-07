from discord.ext import commands
from user_data import UserData
import json
import os


class Clear(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["wipe"], pass_context=True, description="Fully clears your watchlist.")
    async def clear(self, ctx):
        username = str(ctx.author)
        user = UserData.create_user_instance_by_name(username)

        with open(user.get_full_path_for_edit(), "r+") as f:
            print(user.get_full_path_for_edit())
            data = json.load(f)
            data["Watchlist"][0].clear()
            await user.update_watchlist(data)

            await ctx.message.add_reaction("👍")


def setup(client):
    client.add_cog(Clear(client))