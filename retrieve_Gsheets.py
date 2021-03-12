"""
Loads commands from the Telegram Bot Commands Google Sheet.
Outputs commands as commands.json and commands.csv in the data directory.
New commands.json will be used by Telegram bot upon restart of bot.
"""

import requests
import csv
import json


CSV_URL = 'https://docs.google.com/spreadsheets/d/1f_8gSKAnVzEkKSL1xqGAfW8ynZJgt3dNf614ad2MCaI/export?format=csv'
jsonFilePath = 'data/commands.json'
csvFilePath = 'data/commands.csv'
data = {}

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8').replace("'", "’")
    cr = csv.DictReader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    
    for row in my_list:
        key = row['Command']
        data[key] = row

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

    with open(csvFilePath, 'wb') as csvf:
        csvf.write(download.content)
