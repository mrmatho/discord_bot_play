import discord
import requests
import logging
import os
import random


logging.basicConfig(level=logging.INFO)
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logging.info(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("$hello"):
        await handle_hello(message)
    elif message.content.lower().startswith("$bye") or message.content.startswith("$goodbye"):
        await handle_goodbye(message)
    elif message.content.lower().startswith("$help"):
        await handle_help(message)
    elif message.content.lower().startswith("$poem"):
        await handle_poem(message)
    elif message.content.lower().startswith("$afl") or message.content.lower().startswith("$footy"):
        await handle_afl(message)
    elif message.content.lower().startswith("$dice"):
        await handle_dice(message)


async def handle_hello(message):
    await message.channel.send("Hello Legend!")


async def handle_goodbye(message):
    await message.channel.send("Goodbye Legend!")


async def handle_help(message):
    help_message = "Available commands: $hello, $goodbye, $help, $poem, $afl"
    await message.channel.send(help_message)


async def handle_poem(message):
    try:
        response = requests.get("https://poetrydb.org/random")
        response.raise_for_status()
        poem = response.json()[0]
        title = poem["title"]
        author = poem["author"]
        lines = poem["lines"]
        await message.channel.send(f"**{title}** by *{author}*")
        for line in lines[:20]:
            if len(line) > 0:
                await message.channel.send(line)
            else:
                await message.channel.send("...")
        if len(lines) > 20:
            await message.channel.send("... (truncated)")
    except Exception as e:
        logging.error(f"Error fetching poem: {e}")
        await message.channel.send("Sorry, I could not fetch a poem at this time.")
    finally:
        await message.channel.send("~~~")


async def handle_afl(message):
    try:
        header = {"User-Agent": "Cheeky Little Discord Bot - geoffmatheson@gmail.com"}

        response = requests.get(
            "https://api.squiggle.com.au/?q=games;live=1", headers=header
        )
        response.raise_for_status()
        games = response.json()["games"]
        # If there are no live games, show the most recent games
        if len(games) == 0:
            await message.channel.send("No live AFL games at the moment.")
            await message.channel.send("Most recent games completed:")
            response = requests.get(
            "https://api.squiggle.com.au/?q=games;year=2024;complete=100", headers=header)
            response.raise_for_status()
            games = response.json()["games"][-4:]


        for game in games:
            home_team = game["hteam"]
            away_team = game["ateam"]
            home_score = game["hscore"]
            away_score = game["ascore"]
            game_time = game["timestr"]
            home_goals = game["hgoals"]
            home_behinds = game["hbehinds"]
            away_goals = game["agoals"]
            away_behinds = game["abehinds"]
            # Three lines to the message: Home, Away, and Details
            await message.channel.send(
                f"**{home_team}** {home_goals}.{home_behinds}.**{home_score}** "
            )
            await message.channel.send(
                f"**{away_team}** {away_goals}.{away_behinds}.**{away_score}**"
            )
            await message.channel.send(
                f"{game_time}  - *{game['roundname']} - {game['venue']}*"
            )
    except Exception as e:
        logging.error(f"Error fetching AFL scores: {e}")
        logging.error(response.text)
        await message.channel.send(
            "Sorry, I could not fetch the AFL scores at this time."
        )


async def handle_dice(message):
    try:
        dice = message.content.split(" ")[1:]
        if not dice:
            num_dice = 1
            num_sides = 6
        else:
            num_dice = int(dice[0])
            if len(dice) == 1:
                num_sides = 6
            else:
                num_sides = int(dice[1])
    except ValueError:
        await message.channel.send(
            "Unsure of how many dice or sides you want. Defaulting to 1d6."
        )
        num_dice = 1
        num_sides = 6

    try:
        if num_dice > 100 or num_sides > 100 or num_dice < 1 or num_sides < 1:
            await message.channel.send(
                "Please keep the number of dice and sides on each die less than 100 and more than 0."
            )
            return
        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolls)
        if num_dice == 1:
            await message.channel.send(f"Roll: {rolls[0]}")
        else:
            await message.channel.send(f"Rolls: {rolls}\nTotal: {total}")
    except Exception as e:
        logging.error(f"Error rolling dice: {e}")
        await message.channel.send("Sorry, I could not roll the dice at this time.")


# Retrieve the token from the environment variable
token = os.getenv("DISCORD_BOT_TOKEN")
if token is None:
    raise ValueError("No Discord bot token found in environment variables")

client.run(token)
