from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
SUPER_ADMIN = os.getenv('SUPER_ADMIN')
PASSWORD = os.getenv('PASSWORD') 
LOG_CHANNEL_LINK = os.getenv('LOG_CHANNEL_LINK')
LOG_CHANNEL_ID = os.getenv('LOG_CHANNEL_ID')
CHANNEL_ID = os.getenv('CHANNEL_ID')
CHANNEL_LINK = os.getenv('CHANNEL_LINK')
START_MESSAGE_PHOTO = FSInputFile("content/start_message.jpg")
START_MESSAGE_PHOTO2 = FSInputFile("content/start_message2.jpg")


bot_id = BOT_TOKEN.split(":",1)[0]
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
