import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- GANTI INI BOS ---
WELCOME_CHANNEL_ID = 0  # GANTI JADI ID CHANNEL IN-OUT LU!
ROLE_NAME = "Member MVR"

@bot.event
async def on_ready():
    print(f"BOT ONLINE: {bot.user}")

@bot.event
async def on_member_join(member):
    print(f"Ada yang join: {member.name}")
    # Auto Role
    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)
    if role:
        try:
            await member.add_roles(role)
            print(f"Sukses kasih role ke {member.name}")
        except Exception as e:
            print(f"GAGAL KASIH ROLE: {e}")
    # Welcome
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        try:
            await channel.send(f"🎉 Welcome {member.mention} ke MVR! Kamu dapet role {role.mention}!")
        except Exception as e:
            print(f"GAGAL KIRIM WELCOME: {e}")

bot.run(os.getenv("TOKEN"))
