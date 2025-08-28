# from me :)
# Expects: A ".env" file (yes, that is the whole name, just the extension)
# Expects: 2 lines in that file -------
#SNOOPER_TOKEN=BOT TOKEN FROM DISCORD
#SNOOPER_CHANNEL=YOUR CHANNEL
# This bot will only respond inside of the specified channel, and you can control who has access from there.
# Read only for can see but can't interact, etc.

# How to get a bot token:  https://discord.com/developers/applications/

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from minescript import *
import threading
import time

load_dotenv()
TOKEN = os.getenv("SNOOPER_TOKEN")
CHANNEL_ID = int(os.getenv("SNOOPER_CHANNEL"))


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
channel = None
laststatdrop = ''
event_loop = None
@bot.event
async def on_ready():
    global event_loop, channel
    channel = bot.get_channel(CHANNEL_ID)
    bot.loop.create_task(minecraft_loop())
    

    event_loop = asyncio.get_running_loop()
    thread = threading.Thread(target=minescript_side, daemon=True)
    thread.start()
    print(f'2-way relay connected to Discord through: {bot.user} and {get_player().name}')
    asyncio.run_coroutine_threadsafe(
                    send_to_discord(str(world_info())),
                    bot.loop)

@bot.command()
async def ping(ctx):
    if ctx.channel.id == channel.id:
        await ctx.send(getplayerstats())
        

@bot.command()
async def run(ctx, *, message: str):
    if ctx.channel.id == channel.id:
        execute(message)



def getplayerstats():
    stats = [

        "Name: "+str(get_player().name),
        "HP: "+str(player_health()),
        "POS: "+str(tuple(round(coord) for coord in get_player().position))
        #"INV: "+str(player_inventory()) #enable this if you want your chat spammed
    ]
    return str(stats)

async def minecraft_loop():
        await asyncio.sleep(5) # The spaghetti consumes me
def runbot():
    bot.run(TOKEN)

def minescript_side():
    with EventQueue() as event_queue:
        event_queue.register_chat_listener()
        event_queue.register_world_listener()
        while True:
            event = event_queue.get()
            if event.type == EventType.CHAT:
                
                asyncio.run_coroutine_threadsafe(
                    send_to_discord(event.message),
                    bot.loop)
            elif event.type == EventType.WORLD:
                echo(world_info())
    

async def send_to_discord(message):
    if not "discord.http:" in message and not "File " in message:
        if channel:
            await channel.send(message)
        else:
            print("no channel detected! Make sure the right channel ID is in your .env file!")

runbot()