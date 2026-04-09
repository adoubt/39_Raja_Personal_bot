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
PHOTO = FSInputFile("content/photo1.jpg")
PHOTO2 = FSInputFile("content/photo2.jpg")
PHOTO3 = FSInputFile("content/photo3.jpg")
PHOTO4 = FSInputFile("content/photo4.jpg")
PHOTO5 = FSInputFile("content/photo5.jpg")
PHOTO6 = FSInputFile("content/photo6.jpg")

bot_id = BOT_TOKEN.split(":",1)[0]
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
