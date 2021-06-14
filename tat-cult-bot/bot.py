import asyncio
import logging
import random

from aiogram.types import ChatActions, ContentType, ParseMode, InlineQuery, InputMediaPhoto, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import TOKEN
from aiogram import Bot, Dispatcher, executor, types
import keyboards as kb
from messages import *
from db_helper import Session
from models import Event, Facts
from utils import States
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = TOKEN
session = Session()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(state='*', commands=['start'])
async def send_welcome(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[0])
    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
    await bot.send_sticker(message.chat.id, stickers['hello'])
    await asyncio.sleep(1)
    await message.answer(start_text['start_1'])
    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
    await asyncio.sleep(1)
    await message.answer(start_text['start_2'])
    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
    await asyncio.sleep(2)
    await message.answer(start_text['start_3'])
    await bot.send_chat_action(message.from_user.id, ChatActions.TYPING)
    await asyncio.sleep(2)
    await message.answer(start_text['start_4'])
    await asyncio.sleep(1)
    await bot.send_sticker(message.chat.id, stickers['tss'])
    await asyncio.sleep(1)
    await message.answer(start_text['start_5'], reply_markup=kb.start_m)


@dp.message_handler(state='*', regexp='🐟 🐟 🐟')
async def state_menu(message: types.Message):
    await asyncio.sleep(1)
    await bot.send_sticker(message.chat.id, stickers['eat'])
    await asyncio.sleep(1)
    await message.answer(content_text['thanks'], reply_markup=kb.start_r)
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[1])
    await message.answer(content_text['question'], reply_markup=kb.menu_m)


@dp.message_handler(state=States.TEST_STATE_1)
async def select_date(message: types.Message, state: FSMContext):
    user_event_type = message.text
    if user_event_type not in events_type and user_event_type not in teory_type:
        await bot.send_sticker(message.chat.id, stickers['wrong_text'])
        return await message.answer(content_text['mistake'])
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(States.all()[2])
    if user_event_type in events_type:
        query = session.query(Event).filter(Event.event_type==events_type[user_event_type]).all()
        if len(query) == 0:
            await bot.send_sticker(message.chat.id, stickers['cry_cat'])
            await message.answer(content_text['not_query'], reply_markup=kb.menu_m)
            return await state.set_state(States.all()[1])
        i = 0
        inline_btn_3 = InlineKeyboardButton('Сайт 🌎', url=query[i].url)
        inline_kb1 = InlineKeyboardMarkup().row(kb.inline_btn_1, kb.inline_btn_2).add(kb.inline_btn_5).row(kb.inline_btn_4, inline_btn_3)
        await message.answer(content_text['possible'], reply_markup=kb.start_m)
        await message.answer_photo(query[i].image)
        await message.answer(query[i].title, reply_markup=inline_kb1)
        async with state.proxy() as data:
            data['i'] = i
            data['query'] = query
    elif user_event_type in teory_type:
        facts = session.query(Facts).all()
        i = 0
        await message.answer('Только взгляните на это 🤩', reply_markup=kb.start_m)
        async with state.proxy() as data:
            data['facts'] = facts
        await message.answer_photo(facts[i].image)
        return await message.answer(facts[i].facts, reply_markup=kb.inline_kb2)


@dp.callback_query_handler(lambda c: c.data == 'button1', state='*')
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        i = data['i']
        query = data['query']
    if i > 0:
        i -= 1
    else:
        i = len(query) - 1
    inline_btn_3 = InlineKeyboardButton('Сайт 🌎', url=query[i].url)
    inline_kb1 = InlineKeyboardMarkup().row(kb.inline_btn_1, kb.inline_btn_2).add(kb.inline_btn_5).row(kb.inline_btn_4,
                                                                                                       inline_btn_3)
    await bot.edit_message_media(InputMediaPhoto(query[i].image), callback_query.message.chat.id, callback_query.message.message_id - 1)
    await bot.edit_message_text(query[i].title, callback_query.from_user.id, callback_query.message.message_id, reply_markup=inline_kb1)
    async with state.proxy() as data:
        data['i'] = i


@dp.callback_query_handler(lambda c: c.data == 'button2', state='*')
async def process_callback_button2(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        i = data['i']
        query = data['query']
    if i < len(query) - 1:
        i += 1
    else:
        i = 0
    inline_btn_3 = InlineKeyboardButton('Сайт 🌎', url=query[i].url)
    inline_kb1 = InlineKeyboardMarkup().row(kb.inline_btn_1, kb.inline_btn_2).add(kb.inline_btn_5).row(kb.inline_btn_4,
                                                                                                       inline_btn_3)
    await bot.edit_message_media(InputMediaPhoto(query[i].image), callback_query.message.chat.id, callback_query.message.message_id - 1)
    await bot.edit_message_text(query[i].title, callback_query.from_user.id, callback_query.message.message_id, reply_markup=inline_kb1)
    async with state.proxy() as data:
        data['i'] = i


@dp.callback_query_handler(lambda c: c.data == 'button4', state='*')
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        i = data['i']
        query = data['query']
    await bot.answer_callback_query(callback_query.id, query[i].agent_address, show_alert=True)


@dp.callback_query_handler(lambda c: c.data == 'button5', state='*')
async def process_callback_button5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, content_text['develop'], show_alert=True)


@dp.callback_query_handler(lambda c: c.data == 'button6', state='*')
async def process_callback_button5(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        facts = data['facts']
    i = random.randrange(0, len(facts) - 1)
    await bot.edit_message_media(InputMediaPhoto(facts[i].image), callback_query.message.chat.id,
                                 callback_query.message.message_id - 1)
    await bot.edit_message_text(facts[i].facts, callback_query.from_user.id, callback_query.message.message_id,
                                reply_markup=kb.inline_kb2)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)