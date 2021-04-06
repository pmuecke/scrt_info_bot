import discord
import configparser
import json
from discord.ext import commands
import time
import asyncio

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
        msg = await ctx.channel.send("""{val.get('Output')}""")\n
        await asyncio.sleep(60)\n
        await msg.delete()''')
    else:
        commands_text = ""
        more_text = ""
        commands_counter=0
        for key_com, val_com in command_dict.items():
            if (commands_counter < 10) & (key_com != 'commands'):
                if commands_counter == 0:
                    commands_text += f'/more_commands: Commands not listed here\n'    
                commands_text += f'/{key_com}: {val_com.get("Description")}\n'
                commands_counter += 1
                
            elif key_com != 'commands':
                more_text += f'/{key_com}: {val_com.get("Description")}\n'
        exec(f'''@bot.command()\nasync def {key}(ctx):\n
        msg = await ctx.channel.send("""{commands_text}""")\n
        await asyncio.sleep(30)\n
        await msg.delete()''')
        exec(f'''@bot.command()\nasync def more_commands(ctx):\n
        msg = await ctx.channel.send("""{more_text}""")\n
        await asyncio.sleep(30)\n
        await msg.delete()''')  


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(token)