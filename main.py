from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputFile
from config import token
from func import from_gmail_catcher
from keyboards import kb_main, kb_info, kb_main_reg, kb_feedback_aprove
from keyboards import kb_day1, kb_day2, kb_day3, kb_day4, kb_day5, kb_day6
from keyboards import kb_main_admin
from aiogram.dispatcher.filters import Text
from sql import reg_checker, qr_sender
from stateClasses import FeedbackState, AnswerState
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from sql import admin_catcher, quest_insert, answer_caughter,answer_collect
from sql import take_gmail_user, create_table_main, create_table_feedback, create_db
from sql import create_table_admins, create_table_from_gmail, create_table_questions
from tenacity import retry, wait_random


bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

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
    if message.from_id in admin_catcher():
        await bot.send_message(message.from_id, 'Приветствую, тебя админ!', reply_markup=kb_main_admin)
    elif reg_checker(message.from_id):
        await bot.send_message(message.from_id, 'Добрый день, Вы попали в информационного бота "Школа фундаментальных технологий РБПО"!', reply_markup=kb_main_reg)
    elif not reg_checker(message.from_id):
        await bot.send_message(message.from_id,
                               'Добрый день, Вы попали в информационного бота "Школа фундаментальных технологий РБПО"!',
                               reply_markup=kb_main)


@dp.message_handler(Text(equals='Подробнее о цикле лекций'))
async def info(message: types.Message):
    photo = InputFile('images/info.jpg')
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id,'Весь цикл лекций разбит на 6 дней, чтобы прочитать подробнее о каждом, пользуйтесь кнопками', reply_markup=kb_info)


@dp.message_handler(Text(equals='Назад'))
async def back_info(message: types.Message):
    await bot.send_message(message.from_id,'Весь цикл лекций разбит на 6 дней, чтобы прочитать подробнее о каждом, пользуйтесь кнопками', reply_markup=kb_info)


@dp.message_handler(Text(equals='1) Операционные системы'))
async def day1(message: types.Message):
    photo = InputFile('images/day1.jpg')
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id, 'Общая инфа о направлении, которое дается в этот день', reply_markup=kb_day1)


@dp.message_handler(Text(equals='2) Системы управления базами данных'))
async def day2(message: types.Message):
    photo = InputFile('images/day2.jpg')
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id, 'Общая инфа о направлении, которое дается в этот день', reply_markup=kb_day2)


@dp.message_handler(Text(equals='3) Виртуализация и контейнеризация'))
async def day3(message: types.Message):
    photo = InputFile('images/day3.jpg')
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id, 'Общая инфа о направлении, которое дается в этот день', reply_markup=kb_day3)


@dp.message_handler(Text(equals='4) Интерпретаторы'))
async def day4(message: types.Message):
    photo = InputFile('images/day4.jpg')
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id, 'Общая инфа о направлении, которое дается в этот день', reply_markup=kb_day4)


@dp.message_handler(Text(equals='5) Разработка безопасного ПО'))
async def day5(message: types.Message):
    photo = InputFile('images/day5.jpg')
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id, 'Общая инфа о направлении, которое дается в этот день', reply_markup=kb_day5)



@dp.message_handler(Text(equals='6) Композиционный и компонентный анализ'))
async def day6(message: types.Message):
    photo = InputFile('images/day6.jpg')
    await bot.send_photo(message.from_id, photo=photo)
    await bot.send_message(message.from_id, 'Общая инфа о направлении, которое дается в этот день', reply_markup=kb_day6)


@dp.message_handler(Text(equals='Ядро операционной системы "Linux"'))
async def day1_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Георгий Владимирович Курячий (ведущий разработчик <b>ООО «Базальт СПО»</b>).

📚 <b><u>Тема</u></b>:
➡️ Операционные системы на основе ядра Linux: сообщество, дистрибутив, жизненный цикл.

📟 <b><u>Краткое описание</u></b>:
➡️ История участия российских разработчиков в сообществах Linux. Подходы к построению ОС, дистрибутивы Альт, обеспечение практической безопасности ПО.

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Микроядерная операционная система KasperskyOS'))
async def day1_2(message: types.Message):
    text = '''
👩‍💻 <b><u>Докладчики</u></b>:
➡️ Сергей Викторович Рогачев (руководитель отдела разработки безопасной платформы <b>АО «Лаборатория Касперского»</b>);
➡️ Дмитрий Владимирович Шмойлов (руководитель отдела безопасности программных продуктов <b>АО «Лаборатория Касперского»</b>).

📚 <b><u>Тема</u></b>:
➡️ Микроядерные операционные системы. Summa Technologiae.

📟 <b><u>Краткое описание</u></b>:
➡️ Микроядерная архитектура имеет ряд неоспоримых преимуществ перед системами с монолитным ядром. Все больше игроков анонсируют выпуск своих продуктов, основанных на микроядерных ОС.Лекция осветит историю возникновения микроядерной архитектуры, основные этапы ее становления, отличительные особенности, механизмы предлагаемые для решения задач кибербезопасности, обратит внимание на наиболее ярких представителей, как микроядерные ОС встраиваются в процесс безопасной разработки ПО и какое отношение имеют к конструктивной безопасности и shift-left

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️     
'''
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Системы управления базами данных'))
async def day2_1(message: types.Message):
    text = '''
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Иван Евгеньевич Панченко (заместитель генерального директора <b>ООО «Постгрес Профессиональный» / «Postgres Professional»</b>)

📚 <b><u>Тема</u></b>:
➡️ Активно ведем поиск информации 🕵️‍♂️

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ ️️️‍Активно ведем поиск информации 🕵️‍♂️

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️      
'''
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Системы управления базами данных в "Linux"'))
async def day2_2(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Роман Александрович Симаков (директор департамента развития системных продуктов <b>ООО «Ред Софт»</b>)

📚 <b><u>Тема</u></b>:
➡️ Реляционные базы данных и их роль при построении безопасных информационных систем

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ ️Реляционные БД предоставляют множество проверенных и сертифицированных механизмов для обеспечения защиты хранимых данных, которые могут быть использованы при построении Информационных Систем. Это избавляет разработчиков от необходимости самостоятельной реализации и значительно снижает стоимость и сроки проектов. В лекции будут рассмотрены базовые механизмы защиты данных, предоставляемые СУБД и особенности их реализации и применения.

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️     
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Системы виртуализации и контейнеризации'))
async def day3_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Александр Александрович Дубинин (эксперт по информационной безопасности <b>«YADRO»</b>).

📚 <b><u>Тема</u></b>:
➡️ Контейнеризация и виртуализация - вчера, сегодня, завтра.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ ️️‍Активно ведем поиск информации 🕵️‍♂️

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️    
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

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️     
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='JVM Internals'))
async def day4_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Александр Дроздов (руководитель проектов <b>«Axiom JDK»</b>).

📚 <b><u>Тема</u></b>:
➡️ Java VM - внутреннее устройство и принципы работы.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ Активно ведем поиск информации 🕵️‍♂️

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️      
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Интерпретатор Python'))
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

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️     
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Системы сертификации СЗИ ФСТЭК России'))
async def day5_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Виталий Сергеевич Лютиков (заместитель директора <b>ФСТЭК России</b>)

📚 <b><u>Тема</u></b>:
➡️ Системы сертификации СЗИ ФСТЭК России.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ Активно ведем поиск информации 🕵️‍♂️

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️        
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Технологические центры безопасности ядра "Linux"'))
async def day5_2(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Арутюн Ишханович Аветисян (директор, академик РАН <b>ИСП РАН</b>).

📚 <b><u>Тема</u></b>:
➡️ Технологические центры безопасности ядра "Linux".

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ Активно ведем поиск информации 🕵️‍♂️

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️   
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Композиционный анализ сторонних компонентов'))
async def day6_1(message: types.Message):
    text = """
👩‍💻 <b><u>Докладчик</u></b>:
➡️ Алексей Алексеевич Смирнов (генеральный директор <b>ООО «Профископ» / «CodeScoring»</b>).

📚 <b><u>Тема</u></b>:
➡️ Безопасное использование Open Source.

📟 <b><u>Краткое описание</u></b>:
➡️ ️‍ В лекции будут раскрыты вопросы безопасносного использования Open Source компонентов: от постановки вопроса, до конкретных инструментальных возможностей и описаний процессов их применения.

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️   
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
➡️ ️‍ Активно ведем поиск информации 🕵️‍♂️

‼️ <b><u>Начало</u></b>: DD.MM.YYYY в HH:MM‼️    
"""
    await bot.send_message(message.from_id, text, parse_mode="html")


@dp.message_handler(Text(equals='Регистрация'))
async def register(message: types.Message):
    mess = ''
    user = message.from_user.username
    data = take_gmail_user(user)
    if data:

        await bot.send_message(message.from_id, 'Вы зарегистрированы на следующие события:')
        data = [f'День {i}\n' for i in sorted(data, key=lambda x: x.split('. ')[0])]
        print(data)
        for i in data:
            mess += f'{i}\n'
        await bot.send_message(message.from_id, mess)
        await bot.send_message(message.from_id, 'Если Вы хотите зарегистрировать на новое событие:\nhttps://forms.yandex.ru/u/65ba63fbeb61460b91183250/', reply_markup=kb_main_reg)
    # qr_name = qr_maker(message.from_id, 'test')
    # users_register(message.from_id, 'test_day', qr_name)
    else:
        await bot.send_message(message.from_id, 'Вы еще не регистрировались на наши события, пора это исправить, ссылка на регистрацию:\nhttps://forms.yandex.ru/u/65ba63fbeb61460b91183250/', reply_markup=kb_main_reg)


@dp.message_handler(Text(equals='Пропуска'))
async def passer(message: types.Message):
    qr_list = qr_sender(message.from_id)
    for i in qr_list:
        photo = InputFile(f'qr_codes/{i}')
        await bot.send_message(message.from_id, f'{message.from_user.username}, Ваш пропуск на лекцию "пупуппупуп"')
        await bot.send_photo(message.from_id, photo=photo)

#-1002007643494

@dp.message_handler(Text(equals='Обратная связь'))
async def callback(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_id, '❗Для того чтобы задать вопрос нажмите на <b>«Задать вопрос»</b> на клавиатуре. ', reply_markup=kb_feedback_aprove, parse_mode="HTML")


@dp.message_handler(Text(equals='Задать вопрос'))
async def callback_d(message: types.Message):
    await bot.send_message(message.from_id, 'Введите Ваш вопрос, наша группа поддержки оперативно ответит Вам!',
                           reply_markup=kb_feedback_aprove)
    await FeedbackState.take_quest.set()


@dp.message_handler(state=FeedbackState.take_quest)
async def feedback_sender(message: types.Message, state: FSMContext):
    quest_insert(message.text, message.from_id)
    await bot.send_message(message.from_id, 'Ваш вопрос отправлен! Ожидайте ответ', reply_markup= kb_main_reg)
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
            await bot.send_message(message.from_id, 'На подобранный Вам вопрос уже отвечают, вопспользуйтесь кнопкой <b>«Ответить на вопросы»</b> на клавиатуре.', parse_mode='HTML')

    except:
        await bot.send_message(message.from_id, 'Актуальных вопросов нет!')


@dp.message_handler(state=AnswerState.take_response)
async def take_resp(message: types.Message, state: FSMContext):
    await state.update_data(take_response=message.text)
    data = await state.get_data()
    uid = data.get('uid')
    answer_collect(uid,message.text)
    await bot.send_message(data.get('user_id'),message.text)
    await state.finish()
    await bot.send_message(message.from_id, 'Ответ отправлен пользователю!',reply_markup=kb_main_admin)


@retry(wait=wait_random(min=1, max=2))
def main():
    create_db()
    create_table_main()
    create_table_feedback()
    create_table_questions()
    create_table_admins()
    create_table_from_gmail()
    from_gmail_catcher()
    executor.start_polling(dp, skip_updates=True, timeout=20)


if __name__ == '__main__':
    main()
