# -*- coding: utf-8 -*-
from chatterbot import ChatBot

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new ChatBot instance
bot = ChatBot(
    'Hello',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    database='chatterbot-database',
    database_uri='mongodb://172.17.0.1:27017',
)

print('Type something to begin...')

while True:
    try:
        bot_input = bot.get_response(None)
        print("-------------------------------")

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break