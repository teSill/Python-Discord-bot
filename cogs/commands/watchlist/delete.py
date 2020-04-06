from discord.ext import commands


class Delete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def delete(self, ctx, *, user_input):
        pass


def setup(client):
    client.add_cog(Delete(client))