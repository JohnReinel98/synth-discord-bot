import nextcord
from nextcord.ext import commands
from nextcord import Interaction

#local
import utilities as util

class Mod(commands.Cog):

   def __init__(self, client):
      self.client = client

   #config load
   config = util.loadConfig()
   selfServerId = config["self_server_id"]

   @nextcord.slash_command(name = "purge", description = "Deletes an x amount of messages.", guild_ids=[selfServerId])
   async def purge(self, interaction: Interaction, amount: int):
      if interaction.channel.type == nextcord.ChannelType.text:
         async for message in interaction.channel.history(limit=amount):
            try:
               await message.delete()
            except:
               pass
      await interaction.send(content=f'Deleted {amount} message(s)', delete_after=3)

   @nextcord.slash_command(name = "channelpurge", description = "Attempt to delete 99 messages in a channel.", guild_ids=[selfServerId])
   async def chpurge(self, interaction: Interaction):
      channel = interaction.channel
      messages = await channel.history(limit=99).flatten()

      if channel.type == nextcord.ChannelType.text:
         await channel.delete_messages(messages)
      
      await interaction.send(content='Deleted 99 messages', delete_after=3)


def setup(client):
   client.add_cog(Mod(client))