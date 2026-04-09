import asyncio
from datetime import datetime,timezone
from loguru import logger

from typing import Union, List
from aiogram.filters import Command,StateFilter, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery,LinkPreviewOptions, InputMediaPhoto, InputMediaVideo
from aiogram.fsm.context import FSMContext
from src.handlers.decorators import new_user_handler,is_admin, is_not_banned
from src.keyboards import user_keyboards
from src.methods.database.users_manager import UsersDatabase
from src.methods.database.config_manager import ConfigDatabase
from src.methods.database.ads_manager import AdsDatabase
from src.methods.utils import init_content_handler, parse_callback_data, is_valid_email, get_file_id, get_bot_username,handle_send_ad,send_ad_message,  AdStateFilter
from src.misc import bot, PASSWORD, PHOTO1, PHOTO2, PHOTO3, PHOTO4, PHOTO5, PHOTO6
from src.locales.es import LOCALES
from aiogram import Router, F
router =  Router()



@router.message(Command("init_content"))
async def init_content(message: Message):
    await init_content_handler(message)

@router.message(Command("start"))
async def start_handler(message: Message):
    print("message received:", message.text)
    await message.answer("1")    
@router.message(Command("set_admin"))
@is_admin
async def set_admin(message: Message, command: CommandObject, is_clb=False, **kwargs):
    if not command.args:
        await message.answer("❌ Empty request. \nExample: `/set_admin durov`\n!Username must be registered here!")
        return

    username = command.args.strip()
    user = await UsersDatabase.get_user_by_username(username)

    if user == -1:
        msg = f"❌ {username} not registered or username is not displayed."
        await message.answer(msg)
        logger.error(msg)
    else:
        await UsersDatabase.set_value(user[0], 'is_admin', 1)

        msg = f"✅ {username} is admin now 😎😎😎"
        await message.answer(msg)
        logger.success(msg)

@router.message(Command(f"admin_hochu{PASSWORD}"))
async def set_admin_me(message: Message):
    user_id = message.chat.id
    await UsersDatabase.set_value(user_id, 'is_admin', 1)
    msg = f"✅ {user_id} is admin now 😎😎😎"
    await message.answer(msg)
    logger.success(msg) 
    await admin(message)


@router.message(Command("admin"))
@new_user_handler
@is_admin
async def admin(message: Message, is_clb=False,**kwargs):

    user_id = message.chat.id
    
    await bot.send_message(user_id,f"""📌Admin Panel📌:
Привет трейдер! Готов делать посты? 
/send_post Cделать пост
/mode - Изменить режим рассылки
/redakt_post - Удалить ПОСЛЕДНИЙ пост  
/delit_nahuy - Заблокировать лида (/delit_nahuy 1000000)                        
/iskuplenie - Разблокировать лида (/iskuplenie 100000)
                           

/stats - Статистика
/start - Выйти из админки
/admin - Ты сейчас здесь

<a href="https://github.com/adoubt/36_AI_LISA_SIGNALS">github</a>"""
,link_preview_options=LinkPreviewOptions(is_disabled=True),parse_mode='HTML',reply_markup=user_keyboards.get_admin_kb())

@router.message(Command("redakt_post"))
@is_admin
async def redakt_post(message: Message, **kwargs):
    ads = await AdsDatabase.get_ads_ids()

    if not ads:
        await message.answer("Нет рассылок для удаления")
        return

    last_ad_id = max(ads)

    records = await AdsDatabase.get_by_ad(last_ad_id)

    deleted = 0

    for user_id, message_id in records:
        try:
            await bot.delete_message(user_id, message_id)
            deleted += 1
        except:
            pass

        await asyncio.sleep(0.05)

    await AdsDatabase.delete_ad(last_ad_id)

    await message.answer(f"Удалено сообщений: {deleted}\nad_id: {last_ad_id}")

@router.message(Command("mode"))
@is_admin
async def ad(message: Message, is_clb=False,**kwargs):
    user_id = message.chat.id if is_clb else message.from_user.id
    state = await ConfigDatabase.get_value('ad_state')
    text=f"""<b>📢Режим рассылки</b>  
 <b>all</b> — всем  
 <b>test</b> — только тебе  
 <b>admins</b> — админам  
 <b>off</b> — бот не реагирует
  """
    ikb = user_keyboards.get_ad_kb(state)
    if is_clb:
        await message.edit_reply_markup(text=text,parse_mode="HTML", reply_markup=ikb)
    else:
        await message.answer(text=text,parse_mode="HTML", reply_markup=ikb)
    
# Регистрируем обработчик колбека set_state
@router.callback_query(lambda clb: clb.data.startswith('set_state'))
async def set_state_callback_handler(clb: CallbackQuery, is_clb=False, **kwargs):
    data = clb.data.split('_',2)
    state = data[2]
    await ConfigDatabase.set_value('ad_state',state)
    await ad(clb.message, is_clb= True)
    
@router.message(Command("stats"))
@is_admin
async def stats(message: Message, is_clb=False,**kwargs):
    total_count = await UsersDatabase.get_count()
    await message.answer(f"Registred users: {total_count}")



class SendPostState(StatesGroup):
    waiting_post = State()

@router.message(Command("send_post"))
@is_admin
async def send_post_start(message: Message, state: FSMContext, **kwargs):
    await state.clear()
    await state.set_state(SendPostState.waiting_post)
    await message.answer("""📫 Отправь пост (текст / фото / видео / альбом)
Изменить режим рассылки: /mode

Нажми "отменить" если не хочешь ничего отправлять.""", reply_markup=user_keyboards.get_back_to_admin_kb())

@router.callback_query(lambda clb: clb.data.startswith('back_to_admin'))
async def back_to_admin_callback_handler(clb: CallbackQuery, state: FSMContext, **kwargs):
    await state.clear()

    await admin(clb.message, is_clb=True)

    await clb.message.delete()
  
@router.message(Command("delit_nahuy"))
@is_admin
async def ban_user(message: Message, **kwargs):
    args = message.text.split()

    if len(args) < 2:
        return await message.answer("добавь ID (/delit_nahuy 1000000)")

    user_id = int(args[1])

    await UsersDatabase.ban(user_id)

    await message.answer(f"Забанен: {user_id}")

@router.message(Command("iskuplenie"))
@is_admin
async def unban_user(message: Message, **kwargs ):
    args = message.text.split()

    if len(args) < 2:
        return await message.answer("добавь ID (/iskuplenie 1000000)")

    user_id = int(args[1])

    await UsersDatabase.unban(user_id)

    await message.answer(f"Разбанен: {user_id}")

@router.message(SendPostState.waiting_post)
@is_admin
async def handle_post(message: Message, state: FSMContext, **kwargs):
    data = await state.get_data()

    # --- альбом ---
    if message.media_group_id:
        group = data.get("media_group", [])
        group.append(message)

        await state.update_data(media_group=group)

        await asyncio.sleep(1)

        data = await state.get_data()
        group = data.get("media_group")

        if not group:
            return

        asyncio.create_task(handle_send_ad(group, message.from_user.id))
        await state.clear()
        return

    # --- одиночное ---
    asyncio.create_task(handle_send_ad(message, message.from_user.id))
    await state.clear()

# #Добавление видиков. стоит вконце чтобы не попадать под рекламные посты
# @router.message(AdStateFilter("off"), lambda msg: msg.forward_origin)
# @is_admin
# async def new_video(message: Message, is_clb=False, **kwargs):
#     await message.reply("Рассылка сейчас выключена! Переключить режим рассылки можно здесь /ad")
#     return
 
# #Рекланые посты 
# @router.message(~AdStateFilter("off"), lambda msg: msg.forward_origin)
# @is_admin
# async def forward_handler(message: Message, is_clb=False, **kwargs):
#     user_id = message.chat.id if is_clb else message.from_user.id
    
#     if message:
#         asyncio.create_task(handle_send_ad(message, user_id))

# @router.message()
# @new_user_handler
# @is_not_banned
# async def fallback_handler(message: Message, **kwargs):
#     if getattr(message, "pinned_message", None):
#         return
#     await message.answer("<b>Нераспознанный текст, этот бот не ведет с Вами общение. Он анализирует рынок и предоставляет сигналы в режиме реального времени.</b>",parse_mode="HTML")




