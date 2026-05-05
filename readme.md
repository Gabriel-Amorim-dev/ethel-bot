# Ethel-bot
A Discord bot that replies with lyrics when a song written by Ethel Cain (Hayden Anhedonia) name is mentioned in chat.

## Setup
1. Clone this repo
2. Install dependencies:pip install -r requirements.txt
3. Create a `.env` file:
DISCORD_TOKEN=your_discord_token
GENIUS_TOKEN=your_genius_api_token
4. Open `bot.py` and edit the section at the top:
- `ARTIST` — the artist name
- `SONGS` — list of song titles to watch for
- `EMBED_COLOR` — hex color for the embed sidebar
- `REACTION_EMOJI` — emoji the bot reacts with
5. Run: `python bot.py`

## Getting your tokens
- **Discord:** https://discord.com/developers/applications
- **Genius:** https://genius.com/api-clients

## Disclaimer
All lyrics and song titles belong to their respective owners. No copyright infringement intended.
All rights for the songs and lyrics belong to Hayden Anhedonia. This project is a fan-made tool
and is not affiliated with or endorsed by the artist in any way. Lyrics are fetched from
[Genius](https://genius.com) and are not hosted or distributed by this project.



This bot does not store full lyrics; it retrieves and displays
short excerpts dynamically via the Genius API for non-commercial, educational,
and entertainment purposes.

This project complies with the terms of use of the Genius API:
https://genius.com/api-clients

If you are a rights holder and would like content to be removed, please open an
issue or contact the repository owner and it will be addressed promptly.

Note: some lyrics fetched may contain mature themes.
  This bot is intended for servers where members are aware of the artist's content.