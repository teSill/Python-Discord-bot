from pathlib import PurePath
import os.path
import glob
from discord.ext import commands
from user_data import UserData

TOKEN = os.environ.get('DISCORD_TOKEN')
bot_name = "Temflix"
custom_commands = ["find", "commands", "popular", "findactor", "findactress", "findmovie"]

bot = commands.Bot(command_prefix='!temflix ')
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"{bot_name} has come online!")


#@bot.event
#async def on_command_error(ctx, error):
    #await ctx.send(error)


# @bot.command(pass_context=True)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


# @bot.command(pass_context=True)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


#@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message.content = message.content.lower()


# Load cogs
for filename in glob.iglob('./cogs/**', recursive=True):
    if filename.endswith(".py"):
        file_name = os.path.basename(filename[:-3])
        parent_folder_name = PurePath(filename).parent.name
        grandparent_folder_name = PurePath(filename).parent.parent.name
        bot.load_extension(f"cogs.{grandparent_folder_name}.{parent_folder_name}.{file_name}")

bot.run(TOKEN)
