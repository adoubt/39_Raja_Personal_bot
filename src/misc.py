from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN=os.getenv('BOT_TOKEN')
PASSWORD = os.getenv('PASSWORD') 
PHOTO1 = "content/photo1.jpg"
PHOTO2 = "content/photo2.jpg"
PHOTO3 = "content/photo3.jpg"
PHOTO4 = "content/photo4.jpg"
PHOTO5 = "content/photo5.jpg"
PHOTO6 = "content/photo6.jpg"

bot_id = BOT_TOKEN.split(":",1)[0]
bot = Bot(BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
