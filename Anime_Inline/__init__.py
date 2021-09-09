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

