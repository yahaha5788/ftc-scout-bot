import discord
from discord.ext import commands
import discord.utils
from dotenv import dotenv_values

config = dotenv_values("C:/Users/thomp/bots/keys.env")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)

def checkSupercolor(ctx, u):
    role = discord.utils.find(lambda r: r.name == f'sc.{u}', ctx.message.guild.roles)
    if role in u.roles:
        u.remove_roles(role)
        role.delete()

@bot.event
async def on_ready():
    print("Online.")
    await bot.change_presence(activity=discord.Game(name="with colors"))

@bot.command(pass_context=True, brief="A test command to check if the bot is working")
async def test(ctx):
    await ctx.send("Online")

@bot.command(pass_context=True, aliases=['sc'], help="Command format: $supercolor <hexcode>", description="Uses user input of a 6-character hex code to create a role with that color and add it to the user. The color role includes the user's username to avoid name conflicts", brief="Changes nickname color using a hex code input")
async def supercolor(ctx, hexcode):
    if len(hexcode) != 6:
        await ctx.send('Hex code must be 6 characters long, e.g. B900FF.')
        return
    else:
        hex = hexcode
        hexcode = int(hexcode,16)
        usern = ctx.message.author.name
        checkSupercolor(ctx, usern)
        await ctx.guild.create_role(name=f'sc.{usern}', color=discord.Color(hexcode))
        user = ctx.message.author
        role = discord.utils.get(ctx.guild.roles, name=f'sc.{usern}')
        await user.add_roles(role)
        await role.edit(position=len(ctx.guild.roles))
        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hex}.", color=hexcode)
        await ctx.send(embed=colorembed)

@bot.command(pass_context=True, aliases=['cc'], help="Command format: $clearcolor", description="Clears a user's color role", brief="Clears a user's color role")
async def clearcolor(ctx):
    user = ctx.message.author
    usern = user.name
    role = discord.utils.get(ctx.guild.roles, name=f'sc.{usern}')
    await user.remove_roles(role)
    await role.delete()
    embed = discord.Embed(title='Success!', description='Your color role has been removed')
    await ctx.send(embed=embed)
    
   
  
bot.run(config["POLAROID_API_KEY"])