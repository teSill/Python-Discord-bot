import discord
from discord.ext import commands
from globals import GlobalDiscordMethods


class FindActor(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["findactor"], pass_context=True, description="eg. '!temflix findactor rami malek'. Performs "
                                                                       "a more detailed search than the above "
                                                                       "command.")
    async def find_actor(self, ctx, *, user_input):
        await ctx.send("Looking up '%s' - just a second!" % user_input)
        try:
            await GlobalDiscordMethods.display_actor_in_chat(user_input, ctx)
        except:
            await ctx.channel.send(
                "Sorry, I couldn't find an actor/actress with that query! They probably aren't registered on IMDb or "
                "have an incomplete profile.")


def setup(client):
    client.add_cog(FindActor(client))
