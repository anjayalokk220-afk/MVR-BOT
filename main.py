import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# GANTI SESUAI SERVER LU YA
WELCOME_CHANNEL_ID = 1429123456789  # ID channel in-out lu
ROLE_NAME = "Member MVR"  # Nama role yang mau di auto kasih

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} online! Auto-role aktif!")

@bot.event
async def on_member_join(member):
    # 1. AUTO ROLE
    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)
    if role:
        try:
            await member.add_roles(role)
            print(f"✅ Kasih role {ROLE_NAME} ke {member.name}")
        except Exception as e:
            print(f"❌ Gagal kasih role: {e}")
    
    # 2. WELCOME MESSAGE
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title=f"Welcome to MVR! 🏁",
            description=f"{member.mention} baru aja join!\nSekarang jadi {role.mention if role else ROLE_NAME}!",
            color=0x00ff00
        )
        await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        await channel.send(f"👋 {member.name} udah keluar dari MVR. Bye!")

# GANTI TOKEN DI BAWAH PAKE TOKEN BOT GITHUB LU
bot.run(os.getenv("TOKEN"))
