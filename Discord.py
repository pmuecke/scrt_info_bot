import discord
import configparser
import json
from discord.ext import commands
import time

# Config: Load Telegram token
config = configparser.ConfigParser()
config.read("config/config.txt")
token = config["Discord"]["TOKEN"]

# Retrieve latest commands from Gsheets
import retrieve_Gsheets
time.sleep(5)

client = discord.Client()

# Import command dictionary from json file
with open(f'data/commands.json', 'r') as file:
    command_dict = json.load(file)

bot = commands.Bot(command_prefix='/')

for key, val in command_dict.items():
    if key != 'commands':
        exec(f'''@bot.command()\nasync def {key}(ctx):\n 
        await ctx.channel.send("""{val.get('Output')}""")''')
    else:
        commands_text = ""
        for key_com, val_com in command_dict.items():
            commands_text += f'/{key_com}: {val_com.get("Description")}\n'
        exec(f'''@bot.command()\nasync def {key}(ctx):\n
        await ctx.channel.send("""{commands_text}""")''')  

@bot.command()
async def foo(ctx):
    await ctx.send('Hello')
'''
@client.event
async def on_message(message):
    # Prevent reacting on itself
    if message.author == client.user:
        return

    # Loop through all available commands
    for command, val in command_dict.items():
        if command != 'commands':
            msg = val.get("Output").replace('\\n', '\n').replace('\\t', '\t')
        else:
            commands_text = ""
            for key_com, val_com in command_dict.items():
                val_com_output = val_com.get("Description")
                commands_text += f'/{key_com}: {val_com_output}\n'
            msg = commands_text

        # Send message to channel
        if message.content.startswith(f'/{command.lower()}'):
            await message.channel.send(msg)
'''
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(token)
#client.run(token)