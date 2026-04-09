from aiogram.types import KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from typing import Any



def get_subscription_kb(link) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🗝 Подписаться', url=link)],
        [InlineKeyboardButton(text='🔎 Проверить подписку', callback_data="check_subscribe")]
    ])

    return ikb

def remove() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
def get_start_kb(requested:int) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text='Ver vídeos y ganar dinero 📺')],
        [KeyboardButton(text='Reglas 🎯')],
        [KeyboardButton(text='📱 Mi perfil'), KeyboardButton(text='Retirada de dinero  🏧')],
        [KeyboardButton(text='💰 Ganar aún más dinero 💰')]
    ]
    
    if requested == 1:
        buttons[1].append(KeyboardButton(text='Canal'))  # Добавляем кнопку "Канал" в строку с "Reglas 🎯"
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_admin_kb() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text='/send_post'), KeyboardButton(text='/mode'), KeyboardButton(text='/redakt_post')],
        [KeyboardButton(text='/stats')], 
        [KeyboardButton(text='/admin'), KeyboardButton(text='/start')] ]
    
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_ad_kb(state: str) -> InlineKeyboardMarkup:
    states = ["off", "all", "test", "admins"]

    keyboard = [
        [InlineKeyboardButton(text = f"{s}" if state != s else f"• {s} •", callback_data=f"set_state_{s}")]
        for s in states
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_all_videos_kb(videos,current_page:int, total_pages:int)-> InlineKeyboardMarkup:
   
    buttons = []
    for video in videos:
        video_id, file_id,file_name = video[0],video[1],video[3]
        
        buttons = buttons+[InlineKeyboardButton(text=file_name if file_name else str(video_id), callback_data=f"video_{video_id}")]
    pagination = []
    
    pagination.append(InlineKeyboardButton(text='<', callback_data=f"all_videos_{current_page-1}"))
    pagination.append(InlineKeyboardButton(text = f"{current_page+1}/{total_pages}", callback_data="current_page"))

    pagination.append(InlineKeyboardButton(text='>', callback_data=f"all_videos_{current_page+1}"))
    
    if total_pages>1:
        rows=  [[btn] for btn in buttons] + [pagination] 
    else: rows=  [[btn] for btn in buttons] 
    
    ikb = InlineKeyboardMarkup(inline_keyboard=rows)
    return ikb

def get_admin_video_kb(video_id) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Скрыть", callback_data="hide_file")],
        [InlineKeyboardButton(text="Удалить", callback_data=f"delvideo_{video_id}")]])
    return ikb

def get_videos_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Empezar a ver 📺", callback_data="watch")]])
    return ikb

def get_check_balance_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Empezar a ver 📺", callback_data="watch")],
        [InlineKeyboardButton(text="invitaa tus amigos",callback_data ='earn_more')]])
    return ikb

def get_watch_kb(include_earn_more: bool = False) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text="Participar (recibir un premio)", callback_data="receive")]]
    
    if include_earn_more:
        buttons.append([InlineKeyboardButton(text="💰 Ganar aún más dinero 💰", callback_data='earn_more')])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_channel_kb(link:str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Canal',url=link)]])
    return ikb

def get_withdraw_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Únase al canal", url=CHANNEL_LINK)],
        [InlineKeyboardButton(text="comprobar las incripciones", callback_data="verify_member")]
        ])
    return ikb

def get_process_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='salir ↩️', callback_data="exit")]
        ])
    return ikb

def get_receive_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Ganar aún más dinero 💰", callback_data ='earn_more')]])
    return ikb

def get_back_to_admin_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Вернуться в админку", callback_data ='back_to_admin')]])
    return ikb
