import discord
from discord.ext import commands
import os

IN_CHANNEL_ID = 1560713614594277397
OUT_CHANNEL_ID = 1560713667065155584

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"BOT ON: {bot.user}")

@bot.event
async def on_member_join(member):
    if member.bot: return
    ch = bot.get_channel(IN_CHANNEL_ID)
    print(f"JOIN DETECT: {member.name}")
    if ch:
        await ch.send(f"✅ Welcome {member.mention} ke {member.guild.name}!")

@bot.event
async def on_member_remove(member):
    if member.bot: return
    ch = bot.get_channel(OUT_CHANNEL_ID)
    print(f"LEAVE DETECT: {member.name}")
    if ch:
        await ch.send(f"❌ Goodbye {member.name} telah keluar!")

bot.run(os.getenv("DISCORD_TOKEN"))
