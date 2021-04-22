import discord
import configparser
import json
from discord.ext import commands
import time
#import asyncio
import pandas as pd
from discord import utils

# Config: Load Telegram token
config = configparser.ConfigParser()
config.read("config/config.txt")
token = config["Discord"]["TOKEN"]

# Retrieve latest commands from Gsheets
import retrieve_Gsheets
time.sleep(5)


# Import command dictionary from json file
with open(f'data/commands.json', 'r') as file:
    command_dict = json.load(file)

# Import up-to-date ranks from Gsheets
def retrieve_roles():
    CSV_URL = 'https://docs.google.com/spreadsheets/d/14Id3uoFqiQNwPr_uprjm1pZ_B1lcJF-r3n4d9RRJRbE/export?format=csv&gid=392614415'
    rolesjsonFilePath = 'data/roles.json'
    rolescsvFilePath = 'data/roles.csv'

    data = pd.read_csv(CSV_URL, skiprows=9)
    data.drop(data.columns[[0, 1, 2, 3]], axis = 1, inplace = True)
    data.dropna(inplace=True)

    data.to_csv(rolescsvFilePath)
    data.groupby('Ranking')['Discord Handle'].apply(list).to_json(rolesjsonFilePath,indent=4)
    
    data = json.loads(data.groupby('Ranking')['Discord Handle'].apply(list).to_json(indent=4))

    return data

# Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/',intents=intents)

for key, val in command_dict.items():
    if key != 'commands':
        exec(f'''@bot.command()\nasync def {key}(ctx):\n 
        msg = await ctx.channel.send("""{val.get('Output')}""")''')
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

@bot.command(pass_context=True)
#@commands.has_role("Secret Agent")
async def update_roles(ctx):
    print('Starting update_roles command')
    failed_users = []
    try:
        roles_json = retrieve_roles()
    except:
        await ctx.channel.send('Error while retrieving discord handles from Gsheets')

    for role_name, discord_handles in roles_json.items(): 
        for discord_handle in discord_handles:
            discord_handle = discord_handle.encode('utf-8').decode('ascii', 'ignore')
            try:
                if '#' in discord_handle:
                    user = utils.get(ctx.message.guild.members, name = discord_handle.split('#')[0], discriminator = discord_handle.split('#')[1])
                else:
                    user = utils.get(ctx.message.guild.members, name = discord_handle)
                
                if role_name != 'Secret Agent':
                    discord_role_name = f'Secret Agent - {role_name}'
                elif role_name == 'Secret Agent':
                    discord_role_name = 'Secret Agent'
                role = utils.get(ctx.message.guild.roles, name=discord_role_name)
                #print(role, user)

                if (user != None) and (role != None) and (role not in user.roles):
                    await user.add_roles(role)
                elif (user == None) or (role == None):
                    failed_users.append(f'{role_name}: {discord_handle}')
            except:
                failed_users.append(f'{role_name}: {discord_handle}')
    
    # Save all role - users combinations that resulted in an error
    with open(f'data/failed_discordnames.txt', 'w') as file:
        file.write("\n".join(sorted(failed_users)))
        #print(f'Saved Discord names that resulted in an error in {ctx.guild}')
    
    print('Finished update_roles command')

            

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.run(token)