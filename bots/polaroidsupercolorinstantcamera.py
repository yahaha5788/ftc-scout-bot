import discord
from discord.ext import commands
import discord.utils
from dotenv import dotenv_values
import re

config = dotenv_values("C:/Users/thomp/bots/keys.env")


#role syntax: sc.{usern}
#example: sc.yahaha

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="polaroid ", intents=intents)
        
def currentRoleName(hexcode):
    return f"sc.{hexcode}" #never underestimate my laziness      
        
def isValidHex(hexcode):
    checker = r'[0-9A-Fa-f]{6}'
    try:
        is_hex = re.fullmatch(checker, hexcode)
        return True if is_hex else False
    except TypeError:
        return False

async def checkSupercolor(ctx):
    for role in ctx.message.user.roles:
        if role.name.startswith("sc."):
            await ctx.message.user.remove_roles(role)
            if len(role.members) = 0:
                role.delete()

@bot.event
async def on_ready():
    print("Online.")
    await bot.change_presence(activity=discord.Game(name="with colors"))


@bot.command(pass_context=True, brief="A test command to check if the bot is working")
async def test(ctx):
    await ctx.send("Online")

@bot.command(pass_context=True, aliases=['sc'], help="Command format: polaroid supercolor <hexcode>", description="Uses user input of a 6-character hex code to create a role with that color and add it to the user. The color role includes the user's username to avoid name conflicts", brief="Changes nickname color using a hex code input")
async def supercolor(ctx, hexcode=None):
    if isValidHex(hexcode):
        name = currentRoleName(hexcode)
        user = ctx.message.author
        await checkSupercolor(ctx)
        
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role is None:
            await ctx.guild.create_role(name=name, color=discord.Color(int(hexcode, 16)))
            role = discord.utils.get(ctx.guild.roles, name=name)
                    
        await user.add_roles(role)
        await role.edit(position=len(ctx.guild.roles))
        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode and type "polaroid help sc" for info on the command syntax')
        
@bot.command(pass_context=True, aliases=['cc'], help="Command format: polaroid clearcolor", description="Clears a user's color role", brief="Clears a user's color role")
async def clearcolor(ctx):
    checkSupercolor(ctx)
    embed = discord.Embed(title='Success!', description='Your color role has been removed')
    await ctx.send(embed=embed)
    
  
bot.run(config["POLAROID_API_KEY"])