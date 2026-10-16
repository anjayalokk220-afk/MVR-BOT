import discord
from discord.ext import commands
import os, aiohttp, io
from PIL import Image, ImageDraw, ImageFont

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ MVR-BOT IMAGE ONLINE: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="MVR WELCOME IMAGE"))

async def make_welcome_image(member, text1="WELCOME", text2="to MVR Server"):
    # Background
    bg = Image.new("RGB", (800, 300), (30, 30, 40))
    draw = ImageDraw.Draw(bg)

    # Ambil Avatar
    async with aiohttp.ClientSession() as session:
        async with session.get(str(member.display_avatar.url)) as resp:
            avatar_bytes = await resp.read()

    avatar = Image.open(io.BytesIO(avatar_bytes)).resize((200, 200))
    # Bikin bulat
    mask = Image.new("L", (200, 200), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 200, 200), fill=255)
    bg.paste(avatar, (50, 50), mask)

    # Text
    try:
        font_big = ImageFont.truetype("arial.ttf", 50)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()

    draw.text((300, 60), text1, fill=(0, 255, 136), font=font_big)
    draw.text((300, 130), member.name, fill=(255, 255, 255), font=font_big)
    draw.text((300, 200), text2, fill=(200, 200, 200), font=font_small)

    buffer = io.BytesIO()
    bg.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def get_channel(guild):
    for name in ["welcome", "selamat-datang", "general"]:
        for ch in guild.text_channels:
            if name in ch.name.lower():
                return ch
    return guild.system_channel or guild.text_channels[0]

@bot.event
async def on_member_join(member):
    if member.bot: return
    ch = get_channel(member.guild)
    if ch:
        img = await make_welcome_image(member, "WELCOME", f"Member #{member.guild.member_count}")
        file = discord.File(img, filename="welcome.png")
        embed = discord.Embed(description=f"Selamat datang {member.mention} di **{member.guild.name}**!", color=0x00ff88)
        embed.set_image(url="attachment://welcome.png")
        await ch.send(file=file, embed=embed)

@bot.event
async def on_member_remove(member):
    if member.bot: return
    ch = get_channel(member.guild)
    if ch:
        img = await make_welcome_image(member, "GOODBYE", "Semoga balik lagi!")
        file = discord.File(img, filename="goodbye.png")
        embed = discord.Embed(description=f"{member.name} telah keluar 😢", color=0xff4444)
        embed.set_image(url="attachment://goodbye.png")
        await ch.send(file=file, embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
