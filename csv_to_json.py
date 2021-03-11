"""
Loads commands from commands.csv in the config directory.
Outputs commands as commands.json in the config directory.
New commands.json will be used by Telegram bot upon restart of bot.
"""

import csv
import json
 
 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # Create a dictionary
    data = {}
     
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
         
        # Convert each row into a dictionary 
        # and add it to data
        for rows in csvReader:
             
            # Column 'Command' as the primary key
            key = rows['Command']
            data[key] = rows
 
    # Open a json writer, and use the json.dumps() 
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
         
# Driver Code
 
# Add csv and json file paths
csvFilePath = r'config/commands.csv'
jsonFilePath = r'config/commands.json'
 
# Call the make_json function
make_json(csvFilePath, jsonFilePath)