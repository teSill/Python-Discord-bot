from discord.ext import commands
from user_data import UserData, user_dir
import json
import discord


class Watchlist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def watchlist(self, ctx):
        username = str(ctx.author)
        user = UserData.get_new_user_instance_by_name(username)

        with open(user.get_full_path_for_edit(), "r+") as f:
            data = json.load(f)
            watchlist = data["Watchlist"][0]

            embedded_msg = discord.Embed(title=f"{username}'s watchlist", description="", color=0x00ff00)
            for key, value in watchlist.items():
                embedded_msg.add_field(name=key, value=value, inline=False)

            await ctx.send(embed=embedded_msg)

def setup(client):
    client.add_cog(Watchlist(client))