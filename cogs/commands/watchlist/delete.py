from discord.ext import commands
from user_data import UserData
import json


class Delete(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["del", "remove"], pass_context=True, description="Deletes the given title from your "
                                                                                "watchlist.")
    async def delete(self, ctx, *, user_input):
        username = str(ctx.author)
        user = UserData.create_user_instance_by_name(username)

        with open(user.get_full_path_for_edit(), "r+") as f:
            data = json.load(f)
            data["Watchlist"][0].pop(user_input, None)
            await user.update_watchlist(data)

            await ctx.message.add_reaction("👍")


def setup(client):
    client.add_cog(Delete(client))