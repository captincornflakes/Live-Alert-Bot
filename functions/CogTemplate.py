import discord
from discord.ext import commands
import json
import os

class CogTemplate(commands.Cog):
     def __init__(self, bot):
          self.bot = bot
          self.conn = bot.db_connection
          self.cursor = self.conn.cursor()

     def reconnect_database(self):
          try:
               self.conn.ping(reconnect=True, attempts=3, delay=5)
          except Exception as e:
               print(f"Error reconnecting to the database: {e}")
               
     #your code here
     print(f"I am Loaded")


async def setup(bot):
     await bot.add_cog(CogTemplate(bot))
