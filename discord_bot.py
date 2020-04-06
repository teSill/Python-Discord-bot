from pathlib import PurePath
import os.path
import glob
from discord.ext import commands

TOKEN = os.environ.get('DISCORD_TOKEN')
custom_commands = ["find", "commands", "popular", "findactor", "findactress", "findmovie"]

client = commands.Bot(command_prefix='!temflix ')


@client.event
async def on_ready():
    print("Temflix has come online!")


@client.command(pass_context=True)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")


@client.command(pass_context=True)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

for filename in glob.iglob('./cogs/**', recursive=True):
    if filename.endswith(".py"):
        file_name = os.path.basename(filename[:-3])
        parent_folder_name = PurePath(filename).parent.name
        client.load_extension(f"cogs.{parent_folder_name}.{file_name}")


@client.command(pass_context=True)
async def on_message(self, message):
    if message.author == self.user:
        return

    message.content = message.content.lower()


client.run(TOKEN)
