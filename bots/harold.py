import discord
from query_stuff import queries
from click import pass_context
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

@bot.command(pass_context=True, aliases=['topTeam', 'bt'], help='Command format: $bestTeam <region>. If <region> is left blank, the default region is All.', description='Queries the best team from ftcscout.org with an optional region modifier to search within a given region', brief="Gets the best team from ftcscout.org")
async def bestTeam(ctx, region='All'):
    team_info, team_qstats, team_events = queries.getBestTeam(region)
