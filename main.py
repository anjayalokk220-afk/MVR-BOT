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
    print(f"MVR-BOT IN/OUT READY: {bot.user}")

async def make_image(member, title="WELCOME"):
    bg = Image.new("RGB", (800, 300), (25, 25, 35))
    draw = ImageDraw.Draw(bg)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                data = await resp.read()
        av = Image.open(io.BytesIO(data)).resize((200,200))
        mask = Image.new("L", (200,200), 0)
        ImageDraw.Draw(mask).ellipse((0,0,200,200), fill=255)
        bg.paste(av, (50,50), mask)
    except: pass
    draw.text((300, 70), title, fill=(0,255,136) if title=="WELCOME" else (255,80,80), font=ImageFont.load_default())
    draw.text((300, 140), member.name[:20], fill=(255,255,255), font=ImageFont.load_default())
    draw.text((300, 200), f"Member #{member.guild.member_count}", fill=(180,180,180), font=ImageFont.load_default())
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    buf.seek(0)
    return buf

def get_in_channel(guild):
    for ch in guild.text_channels:
        if "in" in ch.name.lower() and "entrance" not in ch.name.lower():
            return ch
    return None

def get_out_channel(guild):
    for ch in guild.text_channels:
        if "out" in ch.name.lower():
            return ch
    return None

@bot.event
async def on_member_join(member):
    if member.bot: return
    ch = get_in_channel(member.guild)
    if not ch: return
    try:
        img = await make_image(member, "WELCOME TO OUR SERVER")
        await ch.send(content=f"Welcome {member.mention} di **{member.guild.name}**! 🎉", file=discord.File(img, "welcome.png"))
    except Exception as e:
        print(f"Welcome IN error: {e}")
        await ch.send(f"Welcome {member.mention}!")

@bot.event
async def on_member_remove(member):
    if member.bot: return
    ch = get_out_channel(member.guild)
    if not ch: return
    try:
        img = await make_image(member, "GOODBYE THANKS FOR COMING")
        await ch.send(content=f"Goodbye **{member.name}** telah keluar 😢", file=discord.File(img, "goodbye.png"))
    except Exception as e:
        print(f"Goodbye OUT error: {e}")
        try:
            await ch.send(f"Goodbye {member.name} telah keluar!")
        except: pass

bot.run(os.getenv("DISCORD_TOKEN"))
