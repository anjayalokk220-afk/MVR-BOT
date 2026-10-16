import discord
from discord.ext import commands
import os
from datetime import datetime

IN_CHANNEL_ID = 1560713614594277397   # in
OUT_CHANNEL_ID = 1560713667065155584  # out

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"READY: {bot.user} - IN:{IN_CHANNEL_ID} OUT:{OUT_CHANNEL_ID}")

@bot.event
async def on_member_join(member):
    if member.bot: return
    ch = bot.get_channel(IN_CHANNEL_ID)
    if not ch: return
    
    embed = discord.Embed(
        title="🚀 MEMBER BARU MENDARAT!",
        description=f"Welcome {member.mention} ke **{member.guild.name}**!\n\n"
                    f"Semoga betah dan jangan lupa baca rules ya! ✨",
        color=0x00FF88,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 Username", value=f"{member.name}", inline=True)
    embed.add_field(name="📊 Member ke", value=f"{member.guild.member_count}", inline=True)
    embed.set_footer(text=f"ID: {member.id}", icon_url=member.guild.icon.url if member.guild.icon else None)
    
    await ch.send(embed=embed)

@bot.event
async def on_member_remove(member):
    if member.bot: return
    ch = bot.get_channel(OUT_CHANNEL_ID)
    if not ch: return

    embed = discord.Embed(
        title="💨 MEMBER CABUT!",
        description=f"**{member.name}** telah meninggalkan **{member.guild.name}**.\n\n"
                    f"Semoga sukses diluar sana! 👋",
        color=0xFF4444,
        timestamp=datetime.now()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 Username", value=f"{member.name}", inline=True)
    embed.add_field(name="📅 Join Date", value=f"<t:{int(member.joined_at.timestamp())}:R>" if member.joined_at else "-", inline=True)
    embed.set_footer(text=f"Bye bye {member.name}!", icon_url=member.guild.icon.url if member.guild.icon else None)

    await ch.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
