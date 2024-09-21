import discord
import requests
import logging
import os
import random

# Setting up logging (so that I can get more info when I need it, but not pollute my screen)
logging.basicConfig(filename='discord.log', encoding='utf-8', level=logging.INFO)

# Boilerplate code from Discord to get the bot working
intents = discord.Intents.default()
intents.message_content = True

# The client is the thing that makes it all work
client = discord.Client(intents=intents)

# Event handling: logs when the bot is ready
@client.event
async def on_ready():
    """
    Called when the bot has successfully connected to the server and is ready to start receiving events.
    """
    logging.info(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    """
    Handles incoming messages and dispatches them to the appropriate handler functions based on the content of the message.
    Parameters:
    - message: The message object representing the incoming message.
    Returns:
    - None
    Example usage:
        await on_message(message)
    """
    
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
    elif message.content.lower().startswith("$wiki"):
        await handle_wiki(message)

async def handle_hello(message):
    """
    Handles the 'hello' command by sending a greeting message to the channel.

    Args:
        message (discord.Message): The message object that triggered the command.

    Returns:
        None
    """
    await message.channel.send("Hello Legend!")


async def handle_goodbye(message):
    await message.channel.send("Goodbye Legend!")


async def handle_help(message):
    help_message = "Available commands: $hello, $goodbye, $help, $poem, $afl, $dice. \n Dice takes two optional arguments: number of dice and number of sides"
    await message.channel.send(help_message)


async def handle_poem(message):
    """
    Fetches a random poem from the PoetryDB API and sends it as a message in a Discord channel.
    Parameters:
    - message: The message object representing the Discord message.
    Returns:
    None
    """
    try:
        response = requests.get("https://poetrydb.org/random")
        response.raise_for_status()
        poem = response.json()[0]
        title = poem["title"]
        author = poem["author"]
        lines = poem["lines"]
        await message.channel.send(f"**{title}** by *{author}*")
        msg = "\n".join(lines[:20])
        if len(lines) > 20:
            msg += "\n... (truncated)"
        await message.channel.send(msg)
    
    # Includes error handling for the requests.get() function    
    except Exception as e:
        logging.error(f"Error fetching poem: {e}")
        await message.channel.send("Sorry, I could not fetch a poem at this time.")
    finally:
        await message.channel.send("~~~")

async def handle_wiki(message):
    """
    Fetches a random Wikipedia article summary and sends it as a message in a Discord channel.
    Parameters:
    - message: The message object representing the Discord message.
    Returns:
    None
    """
    
    try:
        response = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary")
        response.raise_for_status()
        article = response.json()
        
        title = article["title"]
        # summary = article["extract"]
        link = article["content_urls"]["mobile"]["page"]
        imgUrl = article['thumbnail']['source']
        e = discord.Embed(url=imgUrl, description=title, color=0x00ff00)
        await message.channel.send(f"**{title}**")
        await message.channel.send(embed=e)
        await message.channel.send(f"**Link:** {link}")
        
    except Exception as e:
        logging.error(f"Error fetching Wikipedia article: {e}")
        await message.channel.send("Sorry, I could not fetch a Wikipedia article at this time.")
    

async def handle_afl(message):
    """
    Fetches live AFL games and displays their scores to discord.
    If no games currently live, displays the most recent games.

    Parameters:
    - message: The message object representing the command trigger.

    Returns:
    - None

    Raises:
    - Exception: If there is an error fetching the AFL scores.

    """
        # Code to fetch and display AFL scores
        # Error handling code
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
            # Three lines to the message: Home, Away, and Details. Now sending as one message.
            await message.channel.send(
                f"""**{home_team}** {home_goals}.{home_behinds}.**{home_score}** 
                \n**{away_team}** {away_goals}.{away_behinds}.**{away_score}**
                \n {game_time}  - *{game['roundname']} - {game['venue']}*"""
            )
    except Exception as e:
        logging.error(f"Error fetching AFL scores: {e}")
        logging.error(response.text)
        await message.channel.send(
            "Sorry, I could not fetch the AFL scores at this time."
        )


async def handle_dice(message):
    """
    Handle the dice command by rolling the specified number of dice with the specified number of sides.

    Parameters:
    - message (discord.Message): The message object that triggered the command. 
        The content of the message should be in the format "$dice [num_dice] [num_sides]".

    Returns:
    - None

    Raises:
    - None

    """

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
