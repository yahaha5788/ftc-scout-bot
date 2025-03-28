import discord
from discord.ext import commands
import discord.utils
from dotenv import dotenv_values
import re

command_prefix = "polaroid "
activity = discord.Game(name="with colors")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=command_prefix, intents=intents, activity=activity)
        
def currentRoleName(hexcode: str) -> str:
    return f"sc.{hexcode}" #never underestimate my laziness      
        
def isValidHex(hexcode) -> bool:
    if not isinstance(hexcode, str):  
        return False
    return bool(re.fullmatch(r"[0-9A-Fa-f]{6}", hexcode))

def getName(user) -> str:
    return user.nick if user.nick else user.display_name

async def checkSupercolor(ctx):
    for role in ctx.message.author.roles:
        if role.name.startswith("sc."):
            await ctx.message.author.remove_roles(role)
            if len(role.members) == 0:
                await role.delete()

@bot.event
async def on_ready():
    print("Online.")


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
            await role.edit(position=len(ctx.guild.roles))
        await user.add_roles(role)

        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode and type "polaroid help sc" for info on the command syntax')
        
@bot.command(pass_context=True, aliases=['cc'], help="Command format: polaroid clearcolor", description="Clears a user's color role", brief="Clears a user's color role")
async def clearcolor(ctx):
    await checkSupercolor(ctx)
    embed = discord.Embed(title='Success!', description='Your color role has been removed')
    await ctx.send(embed=embed)
    
@bot.command(pass_context=True)
async def currentcolor(ctx):
    user = ctx.message.author
    for role in user.roles:
        if role.name.startswith("sc."):
            hexcode = f"{role.color.value:06X}"
            await ctx.send(f"{getName(user)}'s current color is #{hexcode}.\nCommand: polaroid supercolor {hexcode}")