import discord
from query_stuff import queries
from discord.ext import commands
import discord.utils
from dotenv import dotenv_values
from random import randint


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_ready():
    print("Encoders have been reset")


@bot.command(pass_context=True, aliases=['topTeam', 'bt'], help='Command format: $bestTeam <region>. If <region> is left blank, the default region is All.', description='Queries the best team from ftcscout.org with an optional region modifier to search within a given region', brief="Gets the best team from ftcscout.org")
async def bestTeam(ctx, region='All'):
    team_info, team_qstats, team_events = queries.getBestTeam(region)

@bot.command(pass_context=True, aliases=['qstats'])
async def quickstats(ctx, number):
    
@bot.command(pass_context=True, aliases=['stats'])
async def teamstats(ctx, number):
    
@bot.command(pass_context=True, aliases=['events'])
async def teamevents(ctx, number):
    
@bot.command(pass_context=True, aliases=['info'])
async def teaminfo(ctx, number):
    
@bot.command(pass_context=True, aliases=['8'])
async def eightball(ctx):
    
@bot.command(pass_context=True)
async def dice(ctx, sides=6):
    roll = randint(0, sides) #i don't remeber how discord emoticons work so fix this later
    dicembed=discord.Embed(title=":dice", description=f"You rolled a **{roll}**")
    ctx.send(embed=embed)
 

