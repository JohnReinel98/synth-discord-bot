#large
import nextcord
from nextcord.ext import commands
import os

#local
import utilities as util

#permissions
intents = nextcord.Intents.all()
intents.typing = True

#config load
config = util.loadConfig()

#general bot setup
client = commands.Bot(command_prefix = config["prefix"], intents = intents)

class BotConfig():
    __version__ = "0.0.1"
    __embedcolor__ = 0x00BCE3


# server status
@client.event
async def on_ready():
    game = nextcord.Game("imong mama...")
    await client.change_presence(activity = game)
    print("==========================")
    print("||   Think-bot online.  ||")
    print("==========================")

initial_cogs = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_cogs.append("cogs." + filename[:-3])

if __name__ == '__main__':
    for cog in initial_cogs:
        client.load_extension(cog)

client.run(config["token"])