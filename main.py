import discord
from discord.ext import commands
import random
import json
import asyncio
import lyricsgenius

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

if not GENIUS_TOKEN:
    raise ValueError("GENIUS_ACCESS_TOKEN não definido!")

genius = lyricsgenius.Genius(GENIUS_TOKEN)

genius = lyricsgenius.Genius(GENIUS_TOKEN, skip_non_songs=True, excluded_terms=["(Remix)", "Live"],timeout=15,retries=3)
genius.verbose= False

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix= '!', intents=intents)
bot.disabled_guilds = set()
bot.active = True
semaphore = asyncio.Semaphore(3)


@bot.command()
@commands.has_permissions(administrator=True)
async def toggle_server(ctx):
    guild_id = ctx.guild.id

    if commands.has_permissions(administrator=False):
        await ctx.send(f"**It seems like thy has not the hierarchy to execute this command.**")

    if guild_id in bot.disabled_guilds:
        bot.disabled_guilds.remove(guild_id)
        await ctx.send(f"**Bot has been reactivaded sucefully, It's happening to everybody.**")
    else:
        bot.disabled_guilds.add(guild_id)
        await ctx.send(f"**Bot has been deactivated sucefully(does not answer replies), blessed be the daughters of Cain**")

@toggle_server.error
async def toggle_server_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("**It seems like thy has not the hierarchy to execute this command. Blessed be the daughters of Cain.**")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.guild.id in bot.disabled_guilds:
        if not message.content.startswith('!toggle_server'):
            return
    await bot.process_commands(message)

    content = message.content.lower()
    matched = 0

    songs = [
        "American Teenager", "A House in Nebraska", "Western Nights",
        "Family Tree", "Hard Times", "Thoroughfare", "Gibson Girl",
        "Ptolemaea", "Sun Bleached Flies", "Strangers", "Michelle Pfeiffer",
        "Crush", "God's Country", "Unpunishable", "Inbred", "Two-Headed Mother",
        "Golden Age", "Sunday Morning", "Casings", "Lilies", "Head in the Wall",
        "Dog Days", "Selby Wall", "Growing Pains", "Vulture", "Knuckle Velvet",
        "Carpet Bed", "Vacillator", "Punish", "Houseofpsychoticwomn",
        "Amber Waves", "Dust Bowl", "Waco, Texas", "Fuck Me Eyes", "Janie",
        "Nettles", "A Knock On The Door", "Tempest", "shrug", "Crying During Sex",
        "Age of Delilah", "Earnhardt", "Arsony", "Famous Last Words", "Verona",
        "Homecoming", "Hospital Beds", "Hospital Beds II", "Doe Hunting",
        "Death Rattle", "Highway Horses", "Chappell Hill", "Starvation",
        "Room 209", "Powerline Valley", "Aging Young Woman", "For Sure",
        "Make Room In Hell", "My favorite types of gay porn", "Bambi", "The God",
        "Dying Star", "Football", "Louisiana",
        "Lead Poisoning", "Ad Nauseam", "wrestling in dirty pits", "Mondays",
        "a long unfortunate while", "trucker's chapel",
        "half-cocked", "Misuse Oh", "independence day", "Jesus Loves You",
        "Stomping Ground", "Great wide nowhere", "everytime", "south alabama",
        "my experiences with paranormal", "perverts",
    ]
    artist = "Ethel Cain"

    for song_name in songs:
        if song_name.lower() in content:
            async with semaphore:
                try:
                    song = await asyncio.to_thread(genius.search_song, song_name, artist)

                    if song and song.lyrics:
                        lines = [
                            l for l in song.lyrics.split("\n")
                            if l.strip() and not l.startswith("[")
                        ]

                        if lines:
                            chosen = random.choice(lines)
                            embed = discord.Embed(
                                title=f"_ {song.title}_",
                                description=f"> {chosen}",
                                color=0x7A3B2E
                            )
                            artist_name = getattr(song, "artist", None)


                            if not artist_name and hasattr(song, "primary_artist"):
                                artist_name = song.primary_artist.name

                            embed.set_footer(text=f"— {artist_name or 'Unknown Artist'} • via Genius")
                            embed.set_image(url=song.song_art_image_url)
                            await message.reply(embed=embed)

                except Exception as e:
                    await message.reply(f"Something went terribly wrong: **{e}**")

                try:
                    await message.add_reaction("<:cross:1463625238314221659>")
                except discord.HTTPException:
                    pass

            matched += 1
            if matched >= 5:
                break
bot.run(TOKEN)
