import discord
import requests

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello Legend!')
        
    if message.content.startswith('$bye') or message.content.startswith('$goodbye'):
        await message.channel.send('Goodbye Legend!')
    
    if message.content.startswith('$help'):
        await message.channel.send('Hello Legend! I am your training bot. I can help you with your training. Just type $hello, $bye or $help to get started.')
    
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
                    msg = f"{g['roundname']} - {g['venue']}"
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