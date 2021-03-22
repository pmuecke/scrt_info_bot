"""
Informational Telegram Bot.
Loads commands from commands.json in the data directory.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import configparser
import logging
import json

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
import time

# Config: Load Telegram token
config = configparser.ConfigParser()
config.read("config/config.txt")
token = config["Telegram"]["TOKEN"]

# Retrieve latest commands from Gsheets
import retrieve_Gsheets
time.sleep(5)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Import command dictionary from json file
with open(f'data/commands.json', 'r') as file:
    command_dict = json.load(file)

# Start command to verify the bot is running (not required to start)
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hi! I'm now listening for commands.")

# Help command 
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('''Please use /commands to view all commands. 
    \nFor further assistance please contact one of the moderators.''')

# Create all command functions in the command dictionary
for key, val in command_dict.items():
    if key != 'commands':
        exec(f'''def {key}(update: Update, context: CallbackContext):\n 
        update.message.reply_text('{val.get('Output')}')''')
    else:
        commands_text = ""
        for key_com, val_com in command_dict.items():
            commands_text += f'/{key_com}: {val_com.get("Description")}\\n'
        exec(f'''def {key}(update: Update, context: CallbackContext):\n 
        update.message.reply_text("{commands_text}")''')  

# Update errors
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Main program
def main():
    """Start the bot."""
    # Create the Updater and pass it the bot's token.
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Create start and help commands
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # Create all commands in command dictionary
    for x in command_dict.keys():
        dispatcher.add_handler(CommandHandler(x, eval(x)))

    # Log update errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # The bot will run until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
