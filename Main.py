import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio


load_dotenv()


BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN') 


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
CHANNEL_ID = int(os.getenv('CHANNEL_DISCORD_ID'))


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"{bot.user.name} has connected to channel!")


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Welcome {member.name} to my channel!")


@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"Goodbye {member.name}. See you later!")


@bot.command()
async def clear(ctx, ammount=""):
    ''' Clear messages '''
    if ammount == "" or ammount == "all":
        await ctx.channel.purge(limit=None)
    else:
        await ctx.channel.purge(limit=int(ammount))


async def load():
    for fileName in os.listdir("./cogs"):
        if fileName.endswith(".py"):
            await bot.load_extension(f"cogs.{fileName[:-3]}")


async def main():
    await load()
    await bot.start(BOT_TOKEN)


asyncio.run(main())