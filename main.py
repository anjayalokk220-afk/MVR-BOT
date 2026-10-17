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
    # WAJIB SYNC SLASH COMMAND BIAR MUNCUL
    try:
        synced = await bot.tree.sync()
        print(f"✅ SYNC {len(synced)} SLASH COMMANDS!")
    except Exception as e:
        print(f"❌ GAGAL SYNC: {e}")

@bot.event
async def on_member_join(member):
    print(f"JOIN: {member.name}")
    # 1. KASIH ROLE
    role = discord.utils.get(member.guild.roles, name=ROLE_NAME)
    if role:
        try:
            # Cek hierarchy bot harus diatas role Member MVR!
            if member.guild.me.top_role.position <= role.position:
                print(f"❌ ROLE BOT KURANG TINGGI! Naikin role bot diatas {ROLE_NAME}")
                return
            await member.add_roles(role)
            print(f"✅ SUKSES KASIH ROLE {ROLE_NAME} ke {member.name}")
        except Exception as e:
            print(f"❌ GAGAL KASIH ROLE: {e}")
    
    # 2. WELCOME IN
    channel = bot.get_channel(WELCOME_IN_ID)
    if channel:
        try:
            embed = discord.Embed(
                title="Welcome to MVR! 🏁",
                description=f"{member.mention} baru join! Selamat datang dan selamat jadi {role.mention if role else ROLE_NAME}!",
                color=0x8A2BE2  # Ungu MVR bos
            )
            embed.set_thumbnail(url=member.display_avatar.url)
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

# === INI YANG BIKIN ERROR TADI BOS, /say FIX ===
@bot.tree.command(name="say", description="Kirim announcement MVR")
@discord.app_commands.describe(text="Isi pesan announcement")
async def say(interaction: discord.Interaction, text: str):
    # WAJIB DEFER BIAR GAK "The application did not respond"
    await interaction.response.defer(ephemeral=True)
    
    try:
        # Kirim ke channel tempat command dipake
        embed = discord.Embed(
            title="📢 MOUNT RAVENIX ANNOUNCEMENT",
            description=text,
            color=0xFFD700  # Gold MVR
        )
        embed.set_footer(text=f"By {interaction.user.name} • MVR")
        await interaction.channel.send(embed=embed)
        await interaction.followup.send("✅ Announcement terkirim!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"❌ Gagal: {e}", ephemeral=True)

bot.run(os.getenv("TOKEN"))
