import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_IN_ID = 1560713614594277397
WELCOME_OUT_ID = 1560713667065155584
ROLE_NAME = "Member MVR"

@bot.event
async def on_ready():
    print(f"✅ BOT ONLINE: {bot.user} | Auto-role aktif!")

@bot.event
async def on_member_join(member):
    print(f"JOIN: {member.name}")
    # 1. KASIH ROLE OTOMATIS
    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)
    if role:
        try:
            await member.add_roles(role)
            print(f"✅ SUKSES KASIH ROLE {ROLE_NAME} ke {member.name}")
        except Exception as e:
            print(f"❌ GAGAL KASIH ROLE: {e}")
    
    # 2. KIRIM WELCOME DI CHANNEL IN
    channel = bot.get_channel(WELCOME_IN_ID)
    if channel:
        try:
            embed = discord.Embed(
                title="Welcome to MVR! 🏁",
                description=f"{member.mention} baru join! Selamat datang dan selamat jadi {role.mention if role else ROLE_NAME}!",
                color=0x00ff00
            )
            await channel.send(embed=embed)
        except Exception as e:
            print(f"❌ GAGAL KIRIM WELCOME: {e}")

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_OUT_ID)
    if channel:
        try:
            await channel.send(f"👋 {member.name} udah keluar dari MVR. Bye!")
        except Exception as e:
            print(f"❌ GAGAL KIRIM GOODBYE: {e}")

bot.run(os.getenv("TOKEN"))
