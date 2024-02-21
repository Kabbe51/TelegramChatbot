"""import configparser
from telethon import TelegramClient, events 
from datetime import datetime
import MySQLdb

config = configparser.ConfigParser()
config.read('config.ini')

API_ID = config.get('default', 'api_id')
API_HASH = config.get('default', 'api_hash')
BOT_TOKEN = config.get('default', 'bot_token')
session_name = "sessions/bot"


HOSTNAME = config.get('default', 'hostname')
USERNAME = config.get('default', 'username')
PASSWORD = config.get('default', 'password')
DATABASE = config.get('default', 'database')

client = TelegramClient(session_name, API_ID, API_HASH).start(bot_token=BOT_TOKEN)"""