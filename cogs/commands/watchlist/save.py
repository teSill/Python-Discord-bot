from discord.ext import commands


class Save(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def save(self, ctx):
        pass


def setup(client):
    client.add_cog(Save(client))