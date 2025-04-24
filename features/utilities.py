import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from pytgcalls import PyTgCalls
from dotenv import load_dotenv

load_dotenv() # load .env file

# Telegram app information
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

#with TelegramClient(StringSession(), API_ID, API_HASH) as client:
#    print("Your session string:", client.session.save())

# Telegram userbot information
SESSION_STRING = os.getenv("SESSION_STRING")

client = TelegramClient("bot", API_ID, API_HASH)

pytgcalls = PyTgCalls(client)
