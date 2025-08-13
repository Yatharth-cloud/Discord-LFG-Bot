import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import discord.ext.commands

# Load the secret token from our .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up the bot's intents (permissions)
intents = discord.Intents.default()
intents.message_content = True

# Create a Bot instance
bot = discord.ext.commands.Bot(command_prefix="!", intents=intents)

# This event runs when the bot has successfully connected and is ready
@bot.event
async def on_ready():
    print(f'Success! Logged in as {bot.user}')
    print('Bot is ready and online!')
    # Try to sync the commands with Discord.
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# --- SLASH COMMANDS ---

# 1. Hello Command
@bot.tree.command(name="hello", description="Says hello back to you!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello there, {interaction.user.mention}!")

# 2. LFG Command
@bot.tree.command(name="lfg", description="Create a Looking for Group post.")
@app_commands.describe(game="The name of the game you want to play.", description="A short description of what you're looking for.")
async def lfg(interaction: discord.Interaction, game: str, description: str):
    embed = discord.Embed(
        title=f"Looking for Group: {game}",
        description=description,
        color=discord.Color.green()
    )
    
    if interaction.user.avatar:
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
    else:
        embed.set_author(name=interaction.user.display_name)
    
    await interaction.response.send_message(embed=embed)
    lfg_message = await interaction.original_response()
    await lfg_message.add_reaction('👍')


# Run the bot using the secret token
bot.run(TOKEN)