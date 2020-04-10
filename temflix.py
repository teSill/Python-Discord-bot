from pathlib import PurePath
import os.path
import glob

import discord
from discord.ext import commands
from trivia_manager import TriviaManager

TOKEN = os.environ.get('DISCORD_TOKEN')
bot_name = "Temflix"
custom_commands = ["find", "commands", "popular", "findactor", "findactress", "findmovie"]

prefixes = ["!temflix ", "!t ", "!tem "]

bot = commands.Bot(command_prefix=prefixes)
bot.remove_command("help")


@bot.event
async def on_ready():
    print(f"{bot_name} has come online!")
    TriviaManager.clear_trivia_folder()


#@bot.event
#async def on_command_error(ctx, error):
    #await ctx.send(error)


# @bot.command(pass_context=True)
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


# @bot.command(pass_context=True)
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    #message.content = message.content.lower()

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    trivia_emojis = ["🇦", "🇧", "🇨", "🇩"]
    if user == bot.user:
        return
    if TriviaManager.channel_has_running_game(str(channel.id)):
        if reaction.emoji not in trivia_emojis:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        correct_option = TriviaManager.get_correct_answer(str(channel.id))

        if reaction.emoji == trivia_emojis[0] and correct_option == "a":
            msg = "winner winner chicken dinner"
        elif reaction.emoji == trivia_emojis[1] and correct_option == "b":
            msg = "winner winner chicken dinner"
        elif reaction.emoji == trivia_emojis[2] and correct_option == "c":
            msg = "winner winner chicken dinner"
        elif reaction.emoji == trivia_emojis[3] and correct_option == "d":
            msg = "winner winner chicken dinner"
        else:
            msg = "No!"

        embedded_msg = discord.Embed(title=msg, description="",
                                     color=0x00ff00)

        await channel.send(embed=embedded_msg)

@bot.event
async def on_reaction_remove(reaction, user):
    pass
    #channel = reaction.message.channel.id
    #if TriviaManager.channel_has_running_game(str(channel)):



# Load cogs
for filename in glob.iglob('./cogs/**', recursive=True):
    if filename.endswith(".py"):
        file_name = os.path.basename(filename[:-3])
        parent_folder_name = PurePath(filename).parent.name
        grandparent_folder_name = PurePath(filename).parent.parent.name
        bot.load_extension(f"cogs.{grandparent_folder_name}.{parent_folder_name}.{file_name}")

bot.run(TOKEN)
