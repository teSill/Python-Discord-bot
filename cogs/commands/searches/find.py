import discord
from discord.ext import commands
from discord_globals import GlobalMethods


class Find(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["search"])
    async def find(self, ctx, *, user_input):
        await ctx.channel.send("Looking up '%s' - just a second!" % user_input)
        try:
            await GlobalMethods.display_movie_in_chat(user_input, ctx)
        except:
            print("Couldn't find a movie with given query. Trying to find an actor with it...")
            try:
                await GlobalMethods.display_actor_in_chat(user_input, ctx)
            except:
                print("Couldn't find an actor either")
                await ctx.channel.send("Sorry, I couldn't find a result with that query!")
            return


def setup(client):
    client.add_cog(Find(client))