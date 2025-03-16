import discord
from discord.ext import commands
import discord.utils
from dotenv import dotenv_values
from datetime import datetime

config = dotenv_values("C:/Users/thomp/bots/keys.env")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print("Encoders have been reset")

@bot.command
async def bestTeam(ctx):
    await ctx.send("hell if i know")