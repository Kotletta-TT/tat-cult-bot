from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

start_b = KeyboardButton('🐟 🐟 🐟')

start_m = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
start_m.add(start_b)
start_r = ReplyKeyboardRemove()
start_r.clean()

#TODO Переименовать достопримечательности (слишком длинное название для моб. устройств)

menu_1 = KeyboardButton('Фестивали 🥳')
menu_2 = KeyboardButton('Экскурсии 🚠')
menu_3 = KeyboardButton('Cпектакли 🎭')
menu_4 = KeyboardButton('Достопримечательности 🏰')
menu_5 = KeyboardButton('Выставки 🎨')
menu_6 = KeyboardButton('Мастер-классы 💫')
menu_7 = KeyboardButton('Концерты 🎼')
menu_8 = KeyboardButton('Исторические факты 🧐')

menu_m = ReplyKeyboardMarkup().add(menu_2).insert(menu_8).add(menu_3).insert(menu_4).add(menu_5).insert(menu_6).add(menu_7).insert(menu_1).add(start_b)


# choose_event_1 = KeyboardButton('А есть что то еще?')
# choose_event_2 = KeyboardButton('Давай завтра')
# choose_event_3 = KeyboardButton('Выберу в календаре')
# choose_event_4 = KeyboardButton('Я передумал')

choose_event_m = ReplyKeyboardMarkup(resize_keyboard=True).add(start_b)

inline_btn_1 = InlineKeyboardButton('👈 назад', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('вперед 👉', callback_data='button2')
inline_btn_4 = InlineKeyboardButton('Адрес 📍', callback_data='button4')
inline_btn_5 = InlineKeyboardButton('Календарь событий🗓', callback_data='button5')


inline_btn_6 = InlineKeyboardButton('Еще 😋', callback_data='button6')

inline_kb2 = InlineKeyboardMarkup().add(inline_btn_6)