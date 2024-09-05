import discord

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
    
    

client.run('MTIzNDM1NTQwMTU2NzM3NTM4MA.GgmFAS.7lOYJBEkjA6zbSSARs_7LNP_9aiukdazf09EqU')