from discord.ext import commands
import discord.utils
import random
from dotenv import dotenv_values

config = dotenv_values("C:/Users/thomp/bots/keys.env")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="%", intents=intents)

ball = ['Yes.', "No.", "Maybe.", "Not likely.", "Very likely.", "Try again later."]

@bot.event
async def on_ready():
    print("The robobot is online.")

@bot.command(pass_context=True, brief="A test command to check if the bot is working")
async def test(ctx):
    await ctx.send("Online")

@bot.command()
async def dice(ctx):
    user = str(ctx.message.author)
    dice = str(random.randint(1, 6))
    await ctx.send('**' + user + '** rolled a **' + dice + '**')

@bot.command()
async def eightball(ctx):
    await ctx.send("The :8ball: says:")
    await ctx.send('**' + random.choice(ball) + '**')

bot.run(config["ROBOBOT_KEY"])