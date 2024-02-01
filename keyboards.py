from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main_1 = KeyboardButton('Регистрация')
kb_main_2 = KeyboardButton('Подробнее о цикле лекций')
kb_main_3 = KeyboardButton('Обратная связь')
kb_main.add(kb_main_2, kb_main_3).add(kb_main_1)

kb_main_reg = ReplyKeyboardMarkup(resize_keyboard=True)
kb_main_reg_1 = KeyboardButton('Регистрация')
kb_main_reg_2 = KeyboardButton('Подробнее о цикле лекций')
kb_main_reg_3 = KeyboardButton('Обратная связь')
kb_main_reg_4 = KeyboardButton('Пропуска')
kb_main_reg.add(kb_main_reg_2, kb_main_reg_3).add(kb_main_reg_1, kb_main_reg_4)


kb_info = ReplyKeyboardMarkup(resize_keyboard=True)
kb_info_1 = KeyboardButton('1) Операционные системы')
kb_info_2 = KeyboardButton('2) Системы управления базами данных')
kb_info_3 = KeyboardButton('3) Виртуализация и контейнеризация')
kb_info_4 = KeyboardButton('4) Интерпретаторы')
kb_info_5 = KeyboardButton('5) Разработка безопасного ПО')
kb_info_6 = KeyboardButton('6) Композиционный и компонентный анализ')
kb_info_7 = KeyboardButton('На главный экран')
kb_info.add(kb_info_1).add(kb_info_2).add(kb_info_3).add(kb_info_4).add(kb_info_5).add(kb_info_6).add(kb_info_7)

kb_day1 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_day1_1 = KeyboardButton('Ядро операционной системы "Linux"')
kb_day1_2 = KeyboardButton('Микроядерная операционная система KasperskyOS')
kb_day1_3 = KeyboardButton('Назад')
kb_day1.add(kb_day1_1).add(kb_day1_2).add(kb_day1_3)

kb_day2 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_day2_1 = KeyboardButton('Системы управления базами данных')
kb_day2_2 = KeyboardButton('Системы управления базами данных в "Linux"')
kb_day2_3 = KeyboardButton('Назад')
kb_day2.add(kb_day2_1).add(kb_day2_2).add(kb_day2_3)

kb_day3 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_day3_1 = KeyboardButton('Системы виртуализации и контейнеризации')
kb_day3_2 = KeyboardButton('Построение высоконагруженных сред')
kb_day3_3 = KeyboardButton('Назад')
kb_day3.add(kb_day3_1).add(kb_day3_2).add(kb_day3_3)

kb_day4 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_day4_1 = KeyboardButton('JVM Internals')
kb_day4_2 = KeyboardButton('Интерпретатор Python')
kb_day4_3 = KeyboardButton('Назад')
kb_day4.add(kb_day4_1).add(kb_day4_2).add(kb_day4_3)

kb_day5 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_day5_1 = KeyboardButton('Система сертификации СЗИ ФСТЭК России')
kb_day5_2 = KeyboardButton('Технологические центры безопасности ядра "Linux"')
kb_day5_3 = KeyboardButton('Назад')
kb_day5.add(kb_day5_1).add(kb_day5_2).add(kb_day5_3)

kb_day6 = ReplyKeyboardMarkup(resize_keyboard=True)
kb_day6_1 = KeyboardButton('Композиционный анализ сторонних компонентов')
kb_day6_2 = KeyboardButton('Безопасность инфраструктур под управлением Kubernetes')
kb_day6_3 = KeyboardButton('Назад')
kb_day6.add(kb_day6_1).add(kb_day6_2).add(kb_day6_3)





kb_feedback_aprove = ReplyKeyboardMarkup(resize_keyboard=True)
kb_feedback_aprove_1 = KeyboardButton('Задать вопрос')
kb_feedback_aprove_2 = KeyboardButton('Стоп')
kb_feedback_aprove.add(kb_feedback_aprove_1).add(kb_feedback_aprove_2)