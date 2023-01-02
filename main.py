import discord
import requests
import math
import time
from discord.ext import commands

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

yourKey = "5540350d-71bb-4557-b64a-c3881708df0a"

def get_uuid(username):
    url = 'https://api.mojang.com/users/profiles/minecraft/' + username
    userName = username
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['id']
    else:
        return None

def getLevel(uuid):
    url = "https://api.hypixel.net/player?key=" + yourKey + "&uuid=" + uuid
    response = requests.get(url)
    if response.status_code == 200:
        networkExperience = response.json()["player"]["networkExp"]
        networkLevel = (math.sqrt((2 * networkExperience) + 30625) / 50) - 2.5
        return networkLevel
    else:
        return None
    
def getxp(uuid):
    url = "https://api.hypixel.net/player?key=" + yourKey + "&uuid=" + uuid
    response = requests.get(url)
    if response.status_code == 200:
        networkExperience = response.json()["player"]["networkExp"]
        return networkExperience
    else:
        return None

def log_table(username, dev_id, minecraft_user, hypixel_xp, hypixel_level, channel, request_failed):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    failure_string = "Yes" if request_failed else "No"
    with open("Log.txt", "a") as log_file:
            log_string = f"| {username} | {dev_id} | {minecraft_user} | {hypixel_xp} | {hypixel_level} | {channel} |{failure_string} | {current_time} |"
            log_file.write(f"| {username} | {dev_id} | {minecraft_user} | {hypixel_xp} | {hypixel_level} | {channel} |{failure_string} | {current_time} |\n")
            
    print(log_string)

@bot.command()
async def info(ctx, arg):
    title = "Infomation for " + arg
    hypixel_xp = getxp(get_uuid(arg))
    hypixel_level = getLevel(get_uuid(arg))
    print("https://gen.plancke.io/exp/" + arg + ".png")
    embed=discord.Embed(title=title, description="Bot by SpenGUI#2220", color=0xFF5733)
    ###embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_image(url="https://gen.plancke.io/exp/" + arg + ".png")
    
    embed2 = discord.Embed(color=0xFF5733)
    embed2.set_image(url="https://gen.plancke.io/achievementPoints/" + arg + ".png")
    await ctx.send(embed = embed)
    await ctx.send(embed = embed2)
    log_table(ctx.author.name, ctx.author.id, arg, hypixel_xp, hypixel_level, ctx.channel, hypixel_level)

@bot.command(aliases=["quit"])
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
    await ctx.channel.send("Shutting down...")
    await bot.close()

# EXECUTES THE BOT WITH THE SPECIFIED TOKEN. TOKEN HAS BEEN REMOVED AND USED JUST AS AN EXAMPLE.
bot.run()
