import discord
from discord.ext import commands
import os

# Biar bot bisa baca member join & ganti status
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ BOT ONLINE: {bot.user} - SIAP 24 JAM")
    await bot.change_presence(activity=discord.Game(name="MVR 24 JAM"))

@bot.event
async def on_member_join(member):
    # Cari channel welcome
    channel = discord.utils.get(member.guild.text_channels, name="welcome")
    if not channel:
        channel = member.guild.system_channel
    
    if channel:
        embed = discord.Embed(
            title=f"Welcome {member.name}!",
            description=f"Selamat datang di {member.guild.name}!",
            color=0x00ff00
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        await channel.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
