from pathlib import PurePath
import os.path
import glob
from discord.ext import commands

TOKEN = os.environ.get('DISCORD_TOKEN')
custom_commands = ["find", "commands", "popular", "findactor", "findactress", "findmovie"]

bot = commands.Bot(command_prefix='!temflix ')


@bot.event
async def on_ready():
    print("Temflix has come online!")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


@bot.command(pass_context=True)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


@bot.command(pass_context=True)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.command(pass_context=True)
async def on_message(self, message):
    if message.author == self.user:
        return

    message.content = message.content.lower()


# Load cogs
for filename in glob.iglob('./cogs/**', recursive=True):
    if filename.endswith(".py"):
        file_name = os.path.basename(filename[:-3])
        parent_folder_name = PurePath(filename).parent.name
        bot.load_extension(f"cogs.{parent_folder_name}.{file_name}")

bot.run(TOKEN)
