import discord
from discord.ext import commands
import discord.utils
from discord.ui import View, Button
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

def getUsers(guild, name: str) -> list:
    matches = [member for member in guild.members if member.display_name == name]
    return matches

def findSupercolorRole(user):
    for role in user.roles:
        if role.name.startswith("sc."):
            return role
            
    return None
            
def filterUsers(users: list) -> list:
    filtered_users = []
    
    for user in users:
        if findSupercolorRole(user):
            filtered_users.append(user)
            
    return filtered_users
         
        
async def removeSupercolor(ctx):
    user = ctx.message.author
    role = findSupercolorRole(user)
    if role is None:
        return False
        
    await user.remove_roles(role)
    
    if len(role.members) == 0:
        await role.delete()
        
    return True
                
async def addSupercolor(ctx, hexcode):
    name = currentRoleName(hexcode)
    user = ctx.message.author
        
    role = discord.utils.get(ctx.guild.roles, name=name)
    
    if role is None:
        role = await ctx.guild.create_role(name=name, color=discord.Color(int(hexcode, 16)))
        await role.edit(position=len(ctx.guild.roles))
        
    await user.add_roles(role)


class SelectUser(View):
    def __init__(self, ctx, users):
        super().__init__(timeout=30)
        self.ctx = ctx
        self.selected_user = None
        self.users = users

        for user in users:
            color_role = findSupercolorRole(user)
            if not color_role:
                continue

            button = Button(label=user.display_name, style=discord.ButtonStyle.primary, custom_id=str(user.id))

            button.callback = lambda interaction, user=user: self.buttonMonitor(interaction, user)

            self.add_item(button)

    async def buttonMonitor(self, interaction: discord.Interaction, user):
        if interaction.user == self.ctx.author:
            self.selected_user = user
            self.stop()
            await interaction.response.defer()

    async def userSelection(self):
        await self.wait()
        return self.selected_user
        
    async def on_timeout(self):
        if not self.selected_user:
            embed = discord.Embed(title="Timeout", description="Selection timed out")
            await self.ctx.send(embed=embed)
            
            
@bot.event
async def on_ready():
    print("Online.")


@bot.command(pass_context=True, brief="A test command to check if the bot is working")
async def test(ctx):
    await ctx.send("Online")

@bot.command(pass_context=True, aliases=['sc'], help="Command format: polaroid supercolor <hexcode>", description="Uses user input of a 6-character hex code to create a role with that color and add it to the user. The color role includes the user's username to avoid name conflicts", brief="Changes nickname color using a hex code input")
async def supercolor(ctx, hexcode=None):
    if isValidHex(hexcode):
        await removeSupercolor(ctx)
        await addSupercolor(ctx, hexcode)

        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
    else:
        await ctx.send('Invalid hexcode or input. Make sure your input is a valid hexcode and type "polaroid help sc" for info on the command syntax')
        
@bot.command(pass_context=True, aliases=['cc'], help="Command format: polaroid clearcolor", description="Clears a user's color role", brief="Clears a user's color role")
async def clearcolor(ctx):
    had_role = await removeSupercolor(ctx)
    if had_role:
        embed = discord.Embed(title='Click!*', description='Your color role has been removed')
        await ctx.send(embed=embed)
    else: 
        ctx.send("You do not have a color role")
    
@bot.command(pass_context=True)
async def currentcolor(ctx):
    user = ctx.message.author
    role = findSupercolorRole(user)
    
    if not role:
        ctx.send("You do not have a color role")
        return
        
    hexcode = f"{role.color.value:06X}"
    
    embed = discord.Embed(description=f"{getName(user)}'s current color is #{hexcode}.")
    embed.set_footer("Command: polaroid supercolor {hexcode}")
    await ctx.send(embed=embed)
            
@bot.command(pass_context=True)
async def copycolor(ctx, username):
    users: list = getUsers(ctx.guild, username)
    
    filtered_users = filterUsers(users)
    
    if not filtered_users:
        await ctx.send("User not found, or the user entered does not have a valid color role")
        return
        
    if len(filtered_users) == 1:
        found_user = filtered_users[0]
        
    else:
        await ctx.send("Multiple users found. Select one: ")
        for user in filtered_users:
            color_role = findSupercolorRole(user)
            hexcode = f"{color_role.color.value:06X}"
            
            embed = discord.Embed(title=user.display_name, color=int(hexcode, 16))
            await ctx.send(embed=embed)
            
        selector = SelectUser(ctx, filtered_users)
        await ctx.send(view=selector)
        found_user = await selector.userSelection()

    if found_user:
        hexcode = f"{findSupercolorRole(found_user).color.value:06X}"
        await removeSupercolor(ctx)
        await addSupercolor(ctx, hexcode)
        colorembed = discord.Embed(title='*Click!*', description=f"You have been given the color #{hexcode}.", color=int(hexcode, 16))
        await ctx.send(embed=colorembed)
        