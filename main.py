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
    print(f"MVR-BOT IMAGE ONLINE: {bot.user}")

async def make_welcome_image(member, text1="WELCOME"):
    bg = Image.new("RGB", (800, 300), (30, 30, 40))
    draw = ImageDraw.Draw(bg)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                avatar_bytes = await resp.read()
        avatar = Image.open(io.BytesIO(avatar_bytes)).resize((200, 200))
        mask = Image.new("L", (200, 200), 0)
        ImageDraw.Draw(mask).ellipse((0,0,200,200), fill=255)
        bg.paste(avatar, (50, 50), mask)
    except: pass
    draw.text((300, 80), text1, fill=(0,255,136), font=ImageFont.load_default())
    draw.text((300, 150), member.name, fill=(255,255,255), font=ImageFont.load_default())
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    buf.seek(0)
    return buf

def get_channel(guild):
    for ch in guild.text_channels:
        if "welcome" in ch.name.lower() or "general" in ch.name.lower():
            return ch
    return guild.system_channel or guild.text_channels[0]

@bot.event
async def on_member_join(member):
    if member.bot: return
    ch = get_channel(member.guild)
    try:
        img = await make_welcome_image(member, "WELCOME")
        await ch.send(f"Selamat datang {member.mention} di {member.guild.name}!", file=discord.File(img, "welcome.png"))
    except Exception as e:
        print(f"Welcome error: {e}")
        await ch.send(f"Welcome {member.mention}!")

@bot.event
async def on_member_remove(member):
    if member.bot: return
    ch = get_channel(member.guild)
    try:
        img = await make_welcome_image(member, "GOODBYE")
        await ch.send(f"Goodbye {member.name} 😢", file=discord.File(img, "goodbye.png"))
    except Exception as e:
        print(f"Goodbye error (cek permission!): {e}")
        try:
            await ch.send(f"Goodbye {member.name} telah keluar dari server!")
        except: pass

bot.run(os.getenv("DISCORD_TOKEN"))
