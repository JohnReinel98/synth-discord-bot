import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import random

#local
import utilities as util

class Fun(commands.Cog):

   def __init__(self, client):
      self.client = client

   #config load
   config = util.loadConfig()

   selfServerId = config["self_server_id"]

   # Listeners
   @commands.Cog.listener()
   async def on_message(self, message):

      if message.author == self.client.user:
         return
      
      if ("meme") in message.content.lower():
         await message.channel.send("EZ Meme")
         embed = nextcord.Embed(title = "Memez")
         embed.set_image(url="https://media4.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif?cid=ecf05e4734a3dun2oia20p7q398syn8frrdmmrh7mu5chpob&rid=giphy.gif")
         await message.channel.send(embed=embed)

   # Commands
   @nextcord.slash_command(name = "8ball", description = "Ask 8-ball for a random answer.", guild_ids=[selfServerId])
   async def ball(self, interaction: Interaction, question):
      responses = [
      'That is a resounding no',
      'It is not looking likely',
      'Too hard to tell',
      'It is quite possible',
      'That is a definite yes!',
      'Maybe',
      'There is a good chance'
      ]
      answer = random.choice(responses)
      embed = nextcord.Embed(color=0x00BCE3)
      embed.add_field(name="Question", value=question, inline=False)
      embed.add_field(name="Answer", value=answer, inline=False)
      embed.set_thumbnail(url="https://www.horoscope.com/images-US/games/game-magic-8-ball-no-text.png")
      await interaction.send(embed=embed)

def setup(client):
   client.add_cog(Fun(client))