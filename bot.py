import io
import shutil
import zipfile
import discord
from discord.ext import commands
import os
import json
import tracemalloc
import logging
from utils.github_utils import load_github  # Import the function from github_utils
from utils.database_utils import setup_database_connection  # Import the database utility

#pip install mysql-connector-python
#pip install discord.py
#pip install requests

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
logging.basicConfig(level=logging.INFO, handlers=[handler])

def load_config():
    config_file = "datastores/config.json"
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            print(f"Loaded configuration from {config_file}.")
            return config
    except FileNotFoundError:
        print(f"{config_file} not found...")
        return {}

config = load_config()
load_github(config)  # Call the function with the config

# Define the intents for the bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Prefix and bot initialization
PREFIX = "!"

# Ensure application_id exists in config
application_id = int(config.get('application_id', 0))
bot = commands.AutoShardedBot(command_prefix=PREFIX, intents=intents, application_id=application_id, help_command=None)
bot.config = config  # Store config in bot instance

# Set up the database connection
bot.db_connection = setup_database_connection(config)

# Start memory tracking
tracemalloc.start()

# Function to load all Python files from a directory as extensions
async def load_extensions_from_folder(folder):
    for filename in os.listdir(folder):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module_path = f'{folder}.{module_name}'
            try:
                await bot.load_extension(module_path)
                print(f'Loaded extension: {module_path}')
            except Exception as e:
                print(f'Failed to load extension {module_path}. Reason: {e}')

@bot.event
async def on_ready():
    db_status = config['database'].get('status', 'Online') if 'database' in config else 'Online'
    activity = discord.Activity(type=discord.ActivityType.playing, name=db_status)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print(f"Shard ID: {bot.shard_id}")
    print(f"Total Shards: {bot.shard_count}")

    for shard_id, latency in bot.latencies:
        print(f"Shard ID: {shard_id} | Latency: {latency*1000:.2f}ms")

@bot.event
async def on_guild_join(guild):
    await bot.tree.sync(guild=guild)

# Setup hook to load extensions
async def setup_hook():
    await load_extensions_from_folder('functions')
    await bot.tree.sync()

# Assign setup_hook to the bot
bot.setup_hook = setup_hook

# Run the bot with token
if __name__ == '__main__':
    token = config.get('token', '')
    if token:
        bot.run(token, log_handler=handler, log_level=logging.INFO)
    else:
        print("No token found in config! Please check your config.json file.")
