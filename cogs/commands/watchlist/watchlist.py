from discord.ext import commands
from globals import GlobalDiscordMethods

class Watchlist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def watchlist(self, ctx):
        pass


def setup(client):
    client.add_cog(Watchlist(client))