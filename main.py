import discord
from discord.ext import commands
import os

# Biar bot bisa baca member join & ganti nickname
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ BOT ONLINE: {bot.user} - STANDBY 24 JAM!")
    await bot.change_presence(activity=discord.Game(name="MAVERICK COM"))

@bot.event
async def on_member_join(member):
    # Cari channel welcome
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if not channel:
        channel = member.guild.system_channel
    
    if channel:
        embed = discord.Embed(
            title=f
