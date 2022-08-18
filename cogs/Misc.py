import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import requests, datetime, base64, codecs, random

from urllib.parse import urlencode
from googletrans import Translator

#local
import utilities as util

class Misc(commands.Cog):

   def __init__(self, client):
      self.client = client

   #config load
   config = util.loadConfig()

   start_time = datetime.datetime.utcnow()

   selfServerId = config["self_server_id"]
   weatherKey = config["weather_key"]

   translator = Translator()

   @nextcord.slash_command(name = "test", description = "Test message for synth bot.", guild_ids=[selfServerId])
   async def test(self, interaction: Interaction):
      await interaction.response.send_message("Hello mic test 1...2...3...")

   @nextcord.slash_command(name = "covidstats", description = "Check covid stats globally or by country code.", guild_ids=[selfServerId])
   async def covidstats(self, interaction: Interaction, code = 'global'):
      result = requests.get('https://api.covid19api.com/summary').json()
      embed = nextcord.Embed(color=0x00BCE3)
      embed.set_author(name='Covid-19 Statistics', icon_url='https://www.logolynx.com/images/logolynx/9c/9c73792d3e85a72f8dacdce09db31c1d.png')
      embed.set_thumbnail(url='https://covid19api.com/assets/images/image06.png?v24593178829951')

      if code != 'global':
         for i in result['Countries']:
            if i['CountryCode'] == code:
               country_summary = [
                  {'name': 'New Confirmed:', 'value': i['NewConfirmed']},
                  {'name': 'Total Confirmed:', 'value': i['TotalConfirmed']},
                  {'name': 'New Deaths:', 'value': i['NewDeaths']},
                  {'name': 'Total Deaths:', 'value': i['TotalDeaths']},
                  {'name': 'New Recovered:', 'value': i['NewRecovered']},
                  {'name': 'Total Recovered:', 'value': i['TotalRecovered']},
               ]
               string_result = '\n'.join(str(x['name'] + " `" + str(x['value']) + "`") for x in country_summary)
               embed.add_field(name=i['Country'], value=string_result, inline=False)
      else:
         global_summary = [
            {'name': 'New Confirmed:', 'value': result['Global']['NewConfirmed']},
            {'name': 'Total Confirmed:', 'value': result['Global']['TotalConfirmed']},
            {'name': 'New Deaths:', 'value': result['Global']['NewDeaths']},
            {'name': 'Total Deaths:', 'value': result['Global']['TotalDeaths']},
            {'name': 'New Recovered:', 'value': result['Global']['NewRecovered']},
            {'name': 'Total Recovered:', 'value': result['Global']['TotalRecovered']},
         ]
         string_result = '\n'.join(str(x['name'] + " `" + str(x['value']) + "`") for x in global_summary)
         embed.add_field(name="Global Summary", value=string_result, inline=False)
      embed.add_field(name="Source", value='https://covid19api.com/', inline=False)
      await interaction.send(embed=embed)

   @nextcord.slash_command(name = "weather", description = "Check the weather at the city you searched.", guild_ids=[selfServerId])
   async def weather(self, interaction: Interaction, city):
      if Misc.weatherKey == '':
         print(f"[ERROR]: Weather API key is not present in the config.json file.")
      else:
         try:
            req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Misc.weatherKey}')
            r = req.json()
            temperature = round(float(r["main"]["temp"]) - 273.15, 1)
            lowest = round(float(r["main"]["temp_min"]) - 273.15, 1)
            highest = round(float(r["main"]["temp_max"]) - 273.15, 1)
            weather = r["weather"][0]["main"]
            humidity = round(float(r["main"]["humidity"]), 1)
            wind_speed = round(float(r["wind"]["speed"]), 1)
            em = nextcord.Embed(color=0x00BCE3, description=f'''
            Temperature: `{temperature}`
            Lowest: `{lowest}`
            Highest: `{highest}`
            Weather: `{weather}`
            Humidity: `{humidity}`
            Wind Speed: `{wind_speed}`
            ''')
            em.add_field(name='City', value=city.capitalize())
            em.set_thumbnail(url='https://ak0.picdn.net/shutterstock/videos/1019313310/thumb/1.jpg')
            try:
               await interaction.send(embed=em)
            except:
               await interaction.send(f'''
               Temperature: {temperature}
               Lowest: {lowest}
               Highest: {highest}
               Weather: {weather}
               Humidity: {humidity}
               Wind Speed: {wind_speed}
               City: {city.capitalize()}
               ''')
         except KeyError:
            print(f"[ERROR]: {city} Is not a real city")

   @nextcord.slash_command(name = "botstats", description = "Check current stats of the bot.", guild_ids=[selfServerId])
   async def botstats(self, interaction: Interaction):
      uptime = (datetime.datetime.utcnow() - Misc.start_time)
      hours, rem = divmod(int(uptime.total_seconds()), 3600)
      minutes, seconds = divmod(rem, 60)
      days, hours = divmod(hours, 24)
      if days:
         time = '%s days, %s hours, %s minutes, and %s seconds' % (days, hours, minutes, seconds)
      else:
         time = '%s hours, %s minutes, and %s seconds' % (hours, minutes, seconds)
      
      channel_count = 0
      for guild in self.client.guilds:
         channel_count += len(guild.channels)

      em = nextcord.Embed(color=0x00BCE3)
      em.set_author(name='Think-Bot Stats', icon_url=self.client.user.avatar)
      em.add_field(name=u'\U0001F4AC  Prefix', value=".", inline=False)
      em.add_field(name=u'\U0001F553  Uptime', value=time, inline=False)
      em.add_field(name=u'\u2694  Servers', value=str(len(self.client.guilds)), inline=False)
      em.add_field(name=u'\ud83d\udcd1  Channels', value=str(channel_count), inline=False)

      try:
         mem_usage = '{:.2f} MiB'.format(__import__('psutil').Process().memory_full_info().uss / 1024 ** 2)
      except AttributeError:
         # OS doesn't support retrieval of USS (probably BSD or Solaris)
         mem_usage = '{:.2f} MiB'.format(__import__('psutil').Process().memory_full_info().rss / 1024 ** 2)
      em.add_field(name=u'\U0001F4BE  Memory Usage', value=mem_usage, inline=False)
      em.add_field(name=u'\U00002139  Version', value="0.0.1")
      await interaction.send(content=None, embed=em)

   @nextcord.slash_command(name = "userinfo", description = "Check user info.", guild_ids=[selfServerId])
   async def uinfo(self, interaction: Interaction, user: nextcord.Member):
      if user is None:
         user = interaction.author
      date_format = "%a, %d %b %Y %I:%M %p"
      em = nextcord.Embed(color=0x00BCE3, description=user.mention)
      em.set_author(name=str(user), icon_url=user.avatar)
      em.set_thumbnail(url=user.avatar)
      em.add_field(name="Joined", value=user.joined_at.strftime(date_format))
      em.set_footer(text='ID: ' + str(user.id) + "\tStatus: " + str(user.status).upper())
      return await interaction.send(embed=em)

   @nextcord.slash_command(name = "embedmessage", description = "Embeds inputted message.", guild_ids=[selfServerId])
   async def embed(self, interaction: Interaction, title, description):
      embed = nextcord.Embed(color=0x00BCE3, title=title, description=description)
      await interaction.send(embed=embed)

   @nextcord.slash_command(name = "btc", description = "Check current bitcoin price.", guild_ids=[selfServerId])
   async def btc(self, interaction: Interaction):
      r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,EUR,PHP')
      r = r.json()
      usd = r['USD']
      eur = r['EUR']
      php = r['PHP']
      em = nextcord.Embed(color=0x00BCE3, description=f'USD: `${str(usd)}`\nEUR: `€{str(eur)}`\nPHP: `₱{str(php)}`')
      em.set_author(name='Bitcoin', icon_url='https://cdn.pixabay.com/photo/2013/12/08/12/12/bitcoin-225079_960_720.png')
      await interaction.send(embed=em)

   @nextcord.slash_command(name = "eth", description = "Check current ethereum price.", guild_ids=[selfServerId])
   async def eth(self, interaction: Interaction):
      r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,PHP')
      r = r.json()
      usd = r['USD']
      eur = r['EUR']
      php = r['PHP']
      em = nextcord.Embed(color=0x00BCE3, description=f'USD: `${str(usd)}`\nEUR: `€{str(eur)}`\nPHP: `₱{str(php)}`')
      em.set_author(name='Ethereum', icon_url='https://cdn.discordapp.com/attachments/271256875205525504/374282740218200064/2000px-Ethereum_logo.png')
      await interaction.send(embed=em)

   @nextcord.slash_command(name = "slp", description = "Check current small love potion price.", guild_ids=[selfServerId])
   async def slp(self, interaction: Interaction):
      r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=SLP&tsyms=USD,EUR,PHP')
      r = r.json()
      usd = r['USD']
      eur = r['EUR']
      php = r['PHP']
      em = nextcord.Embed(color=0x00BCE3, description=f'USD: `${str(usd)}`\nEUR: `€{str(eur)}`\nPHP: `₱{str(php)}`')
      em.set_author(name='Small Love Potion', icon_url='https://cryptologos.cc/logos/smooth-love-potion-slp-logo.png')
      await interaction.send(embed=em)

   @nextcord.slash_command(name = "hastebin", description = "Pastes a message into hastebin and generate a link.", guild_ids=[selfServerId])
   async def hastebin(self, interaction: Interaction, message):
      r = requests.post("https://hastebin.com/documents", data=message).json()
      em = nextcord.Embed(color=0x00BCE3)
      em.add_field(name='Hastebin Link:', value=f"<https://hastebin.com/{r['key']}>", inline=False)
      await interaction.send(embed=em)

   @nextcord.slash_command(name = "tinyurl", description = "Converts a link into a TinyURL link.", guild_ids=[selfServerId])
   async def tinyurl(self, interaction: Interaction, link):
      r = requests.get(f'http://tinyurl.com/api-create.php?url={link}').text
      em = nextcord.Embed(color=0x00BCE3)
      em.add_field(name='Shortened Link:', value=r, inline=False)
      await interaction.send(embed=em)

   @nextcord.slash_command(name = "pingweb", description = "Check status of a website.", guild_ids=[selfServerId])
   async def pingweb(self, interaction: Interaction, website):
      em = nextcord.Embed(color=0x00BCE3)
      try:
         link = f'http://{website}'
         r = requests.get(link).status_code
         status = 'down' if r != 200 else 'up'
         em.add_field(name='Website Status:', value=f'Site is {status}, responded with a status code of {r}', inline=False)
      except Exception as e:
         em.add_field(name='Error', value="Please try again.", inline=False)
      await interaction.send(embed=em)

   @nextcord.slash_command(name = "lmgtfy", description = "Search a query via lmgtfy.", guild_ids=[selfServerId])
   async def lmgtfy(self, interaction: Interaction, query): # b'\xfc'
      q = urlencode({"q": query})
      em = nextcord.Embed(color=0x00BCE3)
      em.add_field(name='LMGTFY Link:', value=f'<https://lmgtfy.com/?{q}>', inline=False)
      await interaction.send(embed=em)

   @nextcord.slash_command(name = "uptime", description = "Check uptime of the bot.", guild_ids=[selfServerId])
   async def uptime(self, interaction: Interaction):
      uptime = datetime.datetime.utcnow() - Misc.start_time
      uptime = str(uptime).split('.')[0]
      embed = nextcord.Embed(color=0x00BCE3)
      embed.add_field(name='Uptime', value=f'{uptime}', inline=False)
      await interaction.send(embed=embed)

   @nextcord.slash_command(name = "encode", description = "Encode a message into base64.", guild_ids=[selfServerId])
   async def encode(self, interaction: Interaction, message):
      decoded_stuff = base64.b64encode('{}'.format(message).encode('ascii'))
      encoded_stuff = str(decoded_stuff)
      encoded_stuff = encoded_stuff[2:len(encoded_stuff)-1]
      embed = nextcord.Embed(color=0x00BCE3)
      embed.add_field(name='Base64 Encoded Message', value=encoded_stuff, inline=False)
      await interaction.send(embed=embed)

   @nextcord.slash_command(name = "decode", description = "Decode a base64 into a string message.", guild_ids=[selfServerId])
   async def decode(self, interaction: Interaction, code):
      strOne = (code).encode("ascii")
      pad = len(strOne)%4
      strOne += b"="*pad
      encoded_stuff = codecs.decode(strOne.strip(),'base64')
      decoded_stuff = str(encoded_stuff)
      decoded_stuff = decoded_stuff[2:len(decoded_stuff)-1]
      embed = nextcord.Embed(color=0x00BCE3)
      embed.add_field(name='Base64 Decoded Code', value=decoded_stuff, inline=False)
      await interaction.send(embed=embed)

   @nextcord.slash_command(name = "translate", description = "Translates message from detected language to english.", guild_ids=[selfServerId])
   async def translate(self, interaction: Interaction, message):
      embed = nextcord.Embed(color=0x00BCE3)
      embed.set_author(name='Google Translate', icon_url='https://w7.pngwing.com/pngs/249/19/png-transparent-google-logo-g-suite-google-guava-google-plus-company-text-logo.png')

      try:
         result = self.translator.translate(message, dest='en')
         embed.add_field(name='Original', value=message, inline=False)
         embed.add_field(name='Translated', value=result.text, inline=False)
      except Exception as e:
         embed.add_field(name='Error', value="No translation found.", inline=False)
      await interaction.send(embed=embed)

   @nextcord.slash_command(name = "flipcoin", description = "Flip coins for a random result.", guild_ids=[selfServerId])
   async def flipcoin(self, interaction: Interaction):
      coins = ['heads', 'tails']
      result = random.choice(coins)
      em = nextcord.Embed(color=0x00BCE3, title="Flip Coin", description=result.capitalize())
      await interaction.send(embed=em)

def setup(client):
   client.add_cog(Misc(client))