import asyncio
import os
from sql import users_register
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputFile, ReplyKeyboardRemove
from config import token
from func import from_gmail_catcher
from keyboards import kb_main, kb_info
from keyboards import kb_day1, kb_day2, kb_day3, kb_day4, kb_day5, kb_day6
from keyboards import kb_main_admin
from aiogram.dispatcher.filters import Text
from sql import qr_sender
from stateClasses import FeedbackState, AnswerState
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from sql import admin_catcher, quest_insert, answer_caughter, answer_collect, unloading
from sql import take_gmail_user, create_table_main, create_table_feedback, create_db
from sql import create_table_admins, create_table_from_gmail, create_table_questions
from tenacity import retry, wait_random
from datetime import datetime
from mail import start_sender
from config import DAYS
from tg_notifier import start_notifier
import logging

logging.basicConfig(level=logging.INFO, filename="/logs/Bot.log",
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

bot = Bot(token=token)
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=MemoryStorage(), loop=loop)

'''
@dp.errors_handler(exception=exceptions.NetworkError)
async def error_handler(event):
    print(f'Critical error caused by {event.exception}')
    return True
'''


@dp.message_handler(commands=['start'])
@dp.message_handler(Text(equals='Стоп'))
@dp.message_handler(Text(equals='На главный экран'))
async def start_comm(message: types.Message):
    users_register(message.from_id, message.from_user.username)
    text = '''
👋 Здравствуйте! Перед Вами информационный чат-бот <b>"Школы фундаментальных технологий РБПО"!</b> 

❗  Для получения информации о лекциях, обращения к организаторам или регистрации, воспользуйтесь кнопками
    '''
    if message.from_id in admin_catcher():
        await bot.send_message(message.from_id, 'Приветствую, тебя админ!', reply_markup=kb_main_admin)
    else:
        await bot.send_message(message.from_id, text, reply_markup=kb_main, parse_mode="HTML")


@dp.message_handler(Text(equals='Подробнее о цикле лекций'))
async def info(message: types.Message):
    photo = InputFile('images/info.jpg')
    text = """
💻Весь цикл лекций разбит на 6 тематических дней по 2 лекции в рамках одной фундаментальной информационной технологии каждый.
 
📚Чтобы прочитать подробнее о каждом дне и лекциях, которые пройдут в этот день, воспользуйтесь кнопками на клавиатуре.    
    
"""
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id, text, reply_markup=kb_info)


@dp.message_handler(Text(equals='Назад'))
async def back_info(message: types.Message):
    await bot.send_message(message.from_id,
                           'Весь цикл лекций разбит на 6 дней, чтобы прочитать подробнее о каждом, пользуйтесь кнопками',
                           reply_markup=kb_info)


@dp.message_handler(Text(equals='1) Операционные системы'))
async def day1(message: types.Message):
    text = """
<b>Операционные системы</b> – большая тема первого тематического дня, который пройдет 5 марта и объединит две лекции: 
❗<u>«Операционные системы на основе ядра Linux: сообщество, дистрибутив, жизненный цикл»</u> от ООО «Базальт СПО» 
-<u>«Микроядерные операционные системы. Summa Technologiae»</u> от АО «Лаборатория Касперского» 
"""
    await bot.send_message(message.from_id, text, reply_markup=kb_day1, parse_mode="HTML")


@dp.message_handler(Text(equals='2) Системы управления базами данных'))
async def day2(message: types.Message):
    text = """
<b>Системы управления базами данных</b> – большая тема второго тематического дня, который пройдет в 4-ую неделю марта и объединит две лекции: 
❗<u>«Тема уточняется»</u> от ООО «Постгрес Профессиональный» / «Postgres Professional» 
❗<u>«Реляционные базы данных и их роль при построении безопасных информационных систем»</u> от ООО «Ред Софт» 
    """
    await bot.send_message(message.from_id, text, reply_markup=kb_day2, parse_mode="HTML")


@dp.message_handler(Text(equals='3) Виртуализация и контейнеризация'))
async def day3(message: types.Message):
    text = """
<b>Виртуализация и контейнеризация</b> – большая тема третьего тематического дня, который пройдет во 2-ую неделю апреля и объединит две лекции: 
❗<u>«Контейнеризация и виртуализация - вчера, сегодня, завтра»</u> от «YADRO» 
❗<u>«Построение высоконагруженных сред с применением виртуальной инфраструктуры»</u> от ООО «Базис» 
        """
    await bot.send_message(message.from_id, text, reply_markup=kb_day3, parse_mode="HTML")


@dp.message_handler(Text(equals='4) Интерпретаторы'))
async def day4(message: types.Message):
    text = """
<b>Интерпретаторы</b> – большая тема четвертого тематического дня, который пройдет в 4-ую неделю апреля и объединит две лекции: 
❗<u>«Java VM - внутренний мир виртуальной машины, проблемы JIT компиляции и сборки мусора, организация процесса безопасной разработки ПО»</u> от «Axiom JDK» 
❗<u>«Python - история создания, основные идеи и механизмы»</u> от Независимого open-source разработчика 
            """
    await bot.send_message(message.from_id, text, reply_markup=kb_day4, parse_mode="HTML")


@dp.message_handler(Text(equals='5) Разработка безопасного ПО'))
async def day5(message: types.Message):
    text = """
<b>Разработка безопасного программного обеспечения</b> – большая тема пятого тематического дня, который пройдет во 2-ую неделю мая и объединит две лекции: 
❗<u>«Тема уточняется»</u> от ФСТЭК России
❗<u>«Тема уточняется»</u> от ИСП РАН 
"""
    await bot.send_message(message.from_id, text, reply_markup=kb_day5, parse_mode="HTML")


@dp.message_handler(Text(equals='6) Композиционный и компонентный анализ'))
async def day6(message: types.Message):
    text = """
<b>Композиционный и компонентный анализ</b> – большая тема шестого тематического дня, который пройдет в 4-ую неделю мая и объединит две лекции: 
❗<u>«Безопасное использование Open Source»</u> от ООО «Профископ» / «CodeScoring»
❗<u>«Безопасность инфраструктур под управлением оркестратора Kubernetes»</u> от ООО «КлаудРан» / «Luntry»
    """
    await bot.send_message(message.from_id, text, reply_markup=kb_day6, parse_mode="HTML")


@dp.message_handler(Text(equals='Операционные системы на основе ядра Linux'))
async def day1_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Георгий Владимирович Курячий (ведущий разработчик <b>ООО «Базальт СПО»</b>).

📚 <b><u>Тема</u></b>:
➡️ Операционные системы на основе ядра Linux: сообщество, дистрибутив, жизненный цикл.

📟 <b><u>Краткое описание</u></b>:
➡️ История участия российских разработчиков в сообществах Linux. Подходы к построению ОС, дистрибутивы Альт, обеспечение практической безопасности ПО.

‼️ <b><u>Начало</u></b>: 5 марта 11:00 - 13:00‼️
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Микроядерные операционные системы. Summa Technologiae'))
async def day1_2(message: types.Message):
    text = '''
👩‍💻 <b><u>Докладчики</u></b>:
➡️ Сергей Викторович Рогачев (руководитель отдела разработки безопасной платформы <b>АО «Лаборатория Касперского»</b>);
➡️ Дмитрий Владимирович Шмойлов (руководитель отдела безопасности программных продуктов <b>АО «Лаборатория Касперского»</b>).

📚 <b><u>Тема</u></b>:
➡️ Микроядерные операционные системы. Summa Technologiae.

📟 <b><u>Краткое описание</u></b>:
➡️ Микроядерная архитектура имеет ряд неоспоримых преимуществ перед системами с монолитным ядром. Все больше игроков анонсируют выпуск своих продуктов, основанных на микроядерных ОС.Лекция осветит историю возникновения микроядерной архитектуры, основные этапы ее становления, отличительные особенности, механизмы предлагаемые для решения задач кибербезопасности, обратит внимание на наиболее ярких представителей, как микроядерные ОС встраиваются в процесс безопасной разработки ПО и какое отношение имеют к конструктивной безопасности и shift-left
➡️ https://t.me/bmstu1830/5552
➡️ https://t.me/bmstu1830/5552

‼️ <b><u>Начало</u></b>: 5 марта 13:30 - 15:30‼️     
'''
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Системы управления базами данных'))
async def day2_1(message: types.Message):
    text = '''
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Иван Евгеньевич Панченко (заместитель генерального директора <b>ООО «Постгрес Профессиональный» / «Postgres Professional»</b>).

📚 <b><u>Тема</u></b>:
➡️ Тема уточняется 🔎

‼️ <b><u>Начало</u></b>: Время уточняется‼️      
'''
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Реляционные БД и их роль при построении безопасных ИС'))
async def day2_2(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Роман Александрович Симаков (директор департамента развития системных продуктов <b>ООО «Ред Софт»</b>)

📚 <b><u>Тема</u></b>:
➡️ Реляционные базы данных и их роль при построении безопасных информационных систем

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ ️Реляционные БД предоставляют множество проверенных и сертифицированных механизмов для обеспечения защиты хранимых данных, которые могут быть использованы при построении Информационных Систем. Это избавляет разработчиков от необходимости самостоятельной реализации и значительно снижает стоимость и сроки проектов. В лекции будут рассмотрены базовые механизмы защиты данных, предоставляемые СУБД и особенности их реализации и применения.

‼️ <b><u>Начало</u></b>: Время уточняется‼️     
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Контейнеризация и виртуализация - вчера, сегодня, завтра'))
async def day3_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Александр Александрович Дубинин (эксперт по информационной безопасности <b>«YADRO»</b>).

📚 <b><u>Тема</u></b>:
➡️ Контейнеризация и виртуализация - вчера, сегодня, завтра.

‼️ <b><u>Начало</u></b>: Время уточняется‼️    
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Построение высоконагруженных сред'))
async def day3_2(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчики</u></b>:
➡️ Сорокин Дмитрий Анатольевич (технический директор <b>ООО «Базис»</b>).
➡️ Сорокин Дмитрий Игоревич (руководитель блока разработки ядра платформы <b>ООО «Базис»</b>).

📚 <b><u>Тема</u></b>:
➡️ Построение высоконагруженных сред с применением виртуальной инфраструктуры.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ ️Проблемы и пути их решения при разработки облачной платформы с учетом современных требований.

‼️ <b><u>Начало</u></b>: Время уточняется‼️     
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Java VM - внутренний мир виртуальной машины'))
async def day4_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчики</u></b>:
➡️ Александр Сергеевич Дроздов (руководитель проектов <b>«Axiom JDK»</b>).
➡️ Содокладчик уточняется 🔎

📚 <b><u>Тема</u></b>:
➡️ Java VM - внутреннее устройство и принципы работы.

‼️ <b><u>Начало</u></b>: Время уточняется‼️      
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Python - история создания, основные идеи и механизмы'))
async def day4_2(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Никита Андреевич Соболев (Независимый open-source разработчик).

📚 <b><u>Тема</u></b>:
➡️ Python - история создания, основные идеи и механизмы.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ Многие люди знают и любят Python, но не все знают, как он устроен внутри. Лекция кратко и полно раскроет основные моменты:
- Как из исходного кода получается абстрактное синтаксическое дерево (AST)
- Какие оптимизации можно сделать статически?
- Как из AST получается байткод?
- Какие оптимизации есть на шаге выполнения байткода (Tier1, Tier2, JIT)
- Что такое C-API, и почему он настолько важен для CPython?

Лекция позволит получить представление о том, как работают современные языки программирования, а спикер поделиться интересными идеями для проектов в данной сфере.

‼️ <b><u>Начало</u></b>: Время уточняется‼️     
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='В.С. Лютиков (ФСТЭК России)'))
async def day5_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Виталий Сергеевич Лютиков (заместитель директора <b>ФСТЭК России</b>)

📚 <b><u>Тема</u></b>:
➡️ Системы сертификации СЗИ ФСТЭК России.

‼️ <b><u>Начало</u></b>: Время уточняется‼️        
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Академик РАН А.И.Аветисян (ИСП РАН)'))
async def day5_2(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Арутюн Ишханович Аветисян (директор, академик РАН <b>ИСП РАН</b>).

📚 <b><u>Тема</u></b>:
➡️ Технологические центры безопасности ядра "Linux".

‼️ <b><u>Начало</u></b>: Время уточняется‼️   
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Безопасное использование Open Source'))
async def day6_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Алексей Алексеевич Смирнов (генеральный директор <b>ООО «Профископ» / «CodeScoring»</b>).

📚 <b><u>Тема</u></b>:
➡️ Безопасное использование Open Source.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ В лекции будут раскрыты вопросы безопасносного использования Open Source компонентов: от постановки вопроса, до конкретных инструментальных возможностей и описаний процессов их применения.

‼️ <b><u>Начало</u></b>: Время уточняется‼️   
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Безопасность инфраструктур под управлением Kubernetes'))
async def day6_2(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Дмитрий Сергеевич Евдокимов (генеральный директор <b>ООО «КлаудРан» / «Luntry»</b>).

📚 <b><u>Тема</u></b>:
➡️ Безопасность инфраструктур под управлением оркестратора Kubernetes.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ Лекция рассмотрит тему оркестрации контейнеров и оркестратор Kubernetes, даст возможность посмотреть как на устрйство данной системы, так и на ее безопасность и безопасность контейнеров под ее управлением.

‼️ <b><u>Начало</u></b>: Время уточняется‼️    
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Регистрация'))
async def register(message: types.Message):
    mess = ''
    user = message.from_user.username
    data = take_gmail_user(user)
    if data:
        await bot.send_message(message.from_id, 'Вы зарегистрированы на следующие события:')
        data = [DAYS[i] for i in sorted([int(i.split('.')[0].strip().strip("День")) for i in
                                         data])]  # [f'День {i}\n' for i in sorted(data, key=lambda x: x.split('. ')[0])]
        print(data)
        for i in data:
            mess += f'{i}\n\n'
        await bot.send_message(message.from_id, mess)
        await bot.send_message(message.from_id,
                               'Если Вы хотите зарегистрировать на новое событие:\nhttps://forms.yandex.ru/u/65ba63fbeb61460b91183250/',
                               reply_markup=kb_main)
    # qr_name = qr_maker(message.from_id, 'test')
    # users_register(message.from_id, 'test_day', qr_name)
    else:
        await bot.send_message(message.from_id,
                               'Вы еще не регистрировались на наши события, пора это исправить, ссылка на регистрацию:\nhttps://forms.yandex.ru/u/65ba63fbeb61460b91183250/',
                               reply_markup=kb_main)


@dp.message_handler(Text(equals='Пропуска'))
async def passer(message: types.Message):
    qr_list = qr_sender(message.from_id)
    for i in qr_list:
        photo = InputFile(f'qr_codes/{i}')
        await bot.send_message(message.from_id, f'{message.from_user.username}, Ваш пропуск на лекцию "пупуппупуп"')
        await bot.send_photo(message.from_id, photo=photo)


@dp.message_handler(Text(equals='Обратная связь'))
async def callback(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_id,
                           'Введите Ваш вопрос!\n📛Для того чтобы отменить данный процесс нажмите /cancel',
                           parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    await FeedbackState.take_quest.set()


@dp.message_handler(state=FeedbackState.take_quest)
async def feedback_sender(message: types.Message, state: FSMContext):
    if message.text == '/cancel':
        await state.finish()
        await bot.send_message(message.from_id, 'Вы вышли из режима «Обратная связь»!', reply_markup=kb_main)
        return
    quest_insert(message.text, message.from_id)
    await bot.send_message(message.from_id, 'Ваш вопрос отправлен! Ожидайте ответ', reply_markup=kb_main)
    await state.finish()


@dp.message_handler(Text(equals='Ответить на вопросы'))
async def answering(message: types.Message, state: FSMContext):
    try:
        quest_text, id = answer_caughter(message.from_id)
        if id == message.from_id or id == None:
            mess = f"""
👩‍🎓Автор вопроса: {quest_text['tg_id']}

❓Вопрос: {quest_text['quest']}

❗Введите ответ на вопрос:
        """
            await bot.send_message(message.from_id, mess, reply_markup=kb_main_admin)
            await state.update_data(user_id=quest_text['tg_id'])
            await state.update_data(uid=quest_text['uid'])
            await AnswerState.take_response.set()
        else:
            await bot.send_message(message.from_id,
                                   'На подобранный Вам вопрос уже отвечают, вопспользуйтесь кнопкой <b>«Ответить на вопросы»</b> на клавиатуре.',
                                   parse_mode='HTML')

    except:
        await bot.send_message(message.from_id, 'Актуальных вопросов нет!')


@dp.message_handler(Text(equals='Получить выгрузку с БД'))
async def bd_unload(message: types.Message):
    if not os.path.exists("unload"):
        os.mkdir("unload")
    unloading(message.from_id)
    await message.reply_document(open(f'unload/unload_{message.from_id}.csv', 'rb'))
    await bot.send_message(message.from_id,
                           f'Выгрузка участников из Базы данных по состоянию на {datetime.now().strftime("%H:%M:%S %d.%m.%y")}',
                           reply_markup=kb_main_admin)
    os.remove(f'unload/unload_{message.from_id}.csv')


@dp.message_handler(state=AnswerState.take_response)
async def take_resp(message: types.Message, state: FSMContext):
    await state.update_data(take_response=message.text)
    data = await state.get_data()
    uid = data.get('uid')
    answer_collect(uid, message.text)
    await bot.send_message(data.get('user_id'), message.text)
    await state.finish()
    await bot.send_message(message.from_id, 'Ответ отправлен пользователю!', reply_markup=kb_main_admin)



# @retry(wait=wait_random(min=1, max=2))
def main():
    create_db()
    create_table_main()
    create_table_feedback()
    create_table_questions()
    create_table_admins()
    create_table_from_gmail()
    from_gmail_catcher()

    # TODO: Раскоменти перед рассылкой
    # start_sender()
    # dp.loop.create_task(start_notifier(bot))
    # TODO -----------------------------

    executor.start_polling(dp, skip_updates=True, timeout=20)


if __name__ == '__main__':
    main()
