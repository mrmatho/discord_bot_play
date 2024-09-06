import discord
import requests
import logging

logging.basicConfig(level=logging.ERROR)
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello Legend!')
        
    if message.content.startswith('$bye') or message.content.startswith('$goodbye'):
        await message.channel.send('Goodbye Legend!')
    
    if message.content.startswith('$help'):
        await message.channel.send('Try $AFL, $hello or $goodbye')
    
    if message.content.startswith('$poem'):
        try:
            # Fetch a random poem from poetrydb.org
            header = {'User-Agent': "Cheeky Little Discord Bot - geoffmatheson@gmail.com"}
            url = "https://poetrydb.org/random"
            response = requests.get(url, headers = header)
            await message.channel.send('Here is a random little poem for you:')
            data = response.json()[0]
            logging.info("Poetry JSON: " + str(data))
            await message.channel.send(data['title'] + " by " + data['author'])
            # Setting a max of 20 lines
            if len(data['lines']) > 20:
                lines = data['lines'][:19]
                lines.append('... (truncated)')
            else: 
                lines = data['lines']    
                
                
            # Put each line of the poem into the chat
            for line in lines:
                if len(line) > 0:
                    await message.channel.send(line)
                else: 
                    await message.channel.send('...')
        except Exception as e:
            logging.error(e)
            await message.channel.send('Sorry, I could not get a poem at the moment.')
    
    if message.content.startswith('$afl') or message.content.startswith('$AFL'):
        try:
            header = {'User-Agent': "Cheeky Little Discord Bot - geoffmatheson@gmail.com"}
            url = "https://api.squiggle.com.au/?q=games;live=1"
            response = requests.get(url, headers = header)
            #print(response.text)
            data = response.json()
            games = data['games']
            if games:
                for g in games:
                    print(g)
                    score = f"{g['hteam']} {g['hgoals']}.{g['hbehinds']}.{g['hscore']} vs {g['ateam']} {g['agoals']}.{g['abehinds']}.{g['ascore']}"
                    msg = f"{g['timestr']}. {g['roundname']} - {g['venue']}"
                    updated = f"Updated: {g['updated']}"
                    await message.channel.send(score)
                    await message.channel.send(msg)
                    await message.channel.send(updated)
            else:
                await message.channel.send('No games are currently live.')
        except Exception as e:
            print(e)
            await message.channel.send('Sorry, I could not get the AFL scores at the moment.')
        

client.run('MTIzNDM1NTQwMTU2NzM3NTM4MA.GgmFAS.7lOYJBEkjA6zbSSARs_7LNP_9aiukdazf09EqU')