import os
import discord
#from dotenv import load_dotenv

class Data:
    dog = "jmoi"

    def set_name(new_name):
        Data.dog=new_name

print(Data.dog)
Data.set_name("sam2")
print(Data.dog)

#load_dotenv()
TOKEN = os.environ.get('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)


