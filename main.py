import discord
from discord.ext import commands
import os, aiohttp, io
from PIL import Image, ImageDraw, ImageFont

IN_CHANNEL_ID = 1558773339252727818
OUT_CHANNEL_ID = 1558771912275140672

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"MVR-BOT FINAL READY: {bot.user}")
    print(f"IN ID: {IN_CHANNEL_ID} | OUT ID: {OUT_CHANNEL_ID}")

async def make_image(member, title="WELCOME"):
    bg = Image.new("RGB", (800, 350), (25, 25, 35))
    draw = ImageDraw.Draw(bg)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(str(member.display_avatar.url)) as resp:
                data = await resp.read()
        av = Image.open(io.BytesIO(data)).resize((200,200))
        mask = Image.new("L", (200,200), 0)
        ImageDraw.Draw(mask).ellipse((0,0,200,200), fill=255)
        bg.paste(av, (50,75), mask)
    except: pass
    # Warna beda buat welcome & goodbye
    color = (0,255,136) if title == "WELCOME" else (255,70,70)
    draw.text((300, 80), title, fill=color, font=ImageFont.load_default())
    draw.text((300, 140), member.name[:20], fill=(255,255,255), font=ImageFont.load_default())
    draw.text((300, 200), f"Member #{member.guild.member_count}", fill=(180,180,180), font=ImageFont.load_default())
    buf = io.BytesIO()
    bg.save(buf, format="PNG")
    buf.seek(0)
    return buf

@bot.event
async def on_member_join(member):
    if member.bot: return
    ch = member.guild.get_channel(IN_CHANNEL_ID)
    if not ch:
        print("CHANNEL IN GAK KETEMU!")
        return
    try:
        img = await make_image(member, "WELCOME TO OUR SERVER")
        await ch.send(content=f"Welcome {member.mention} ke **{member.guild.name}**! 🎉", file=discord.File(img, "welcome.png"))
        print(f"WELCOME terkirim ke IN")
    except Exception as e:
        print(f"Error IN: {e}")
        try: await ch.send(f"Welcome {member.mention}!")
        except: pass

@bot.event
async def on_member_remove(member):
    if member.bot: return
    ch = member.guild.get_channel(OUT_CHANNEL_ID)
    if not ch:
        print("CHANNEL OUT GAK KETEMU!")
        return
    try:
        img = await make_image(member, "GOODBYE THANKS FOR COMING")
        await ch.send(content=f"Goodbye **{member.name}** telah keluar 😢", file=discord.File(img, "goodbye.png"))
        print(f"GOODBYE terkirim ke OUT")
    except Exception as e:
        print(f"Error OUT: {e}")
        try: await ch.send(f"Goodbye {member.name} telah keluar!")
        except: pass

bot.run(os.getenv("DISCORD_TOKEN"))
