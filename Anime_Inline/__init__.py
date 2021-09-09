import os
import sys
import logging
import time
from telegraph import Telegraph
from Anime_Inline.config import Config
from pyrogram import Client, filters, errors
from jikanpy import Jikan
StartTime = time.time()
logging.basicConfig(level=logging.INFO)

LOGGER = logging.getLogger(__name__)

telegraph = Telegraph()
telegraph.create_account(short_name='anime')

API_ID = os.environ.get('API_ID', None)
API_HASH = os.environ.get('API_HASH', None)
BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
ALLOWED_USERS = [
        1809105906
    ]
LOG_CHANNEL = os.environ.get('LOG_CHANNEL', None)
OWNER_USERNAME = os.environ.get('OWNER_USERNAME', None)
BOT_USERNAME = os.environ.get('BOT_USERNAME', None)
BOT_NAME = os.environ.get('BOT_NAME', None)
INLINE_PIC = os.environ.get('INLINE_PIC', None)
INLINE_PIC_1 = os.environ.get('INLINE_PIC_1', None)

jikan = Jikan()
ANIME = Client("Anime", api_id = API_ID, api_hash = API_HASH, bot_token = BOT_TOKEN)
with ANIME:
    botname = ANIME.get_me().username
