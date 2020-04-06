import discord
from discord.ext import commands
from globals import GlobalDiscordMethods


class FindActress(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["findactress"], pass_context=True)
    async def find_actress(self, ctx, *, user_input):
        await ctx.send("Looking up '%s' - just a second!" % user_input)
        try:
            await GlobalDiscordMethods.display_actor_in_chat(user_input, ctx)
        except:
            await ctx.channel.send(
                "Sorry, I couldn't find an actor/actress with that query! They probably aren't registered on IMDb or have an incomplete profile.")


def setup(client):
    client.add_cog(FindActress(client))