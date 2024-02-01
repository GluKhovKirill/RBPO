from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import InputFile
from config import token
from func import qr_maker, data_maker
from keyboards import kb_main, kb_info, kb_main_reg, kb_feedback_aprove
from keyboards import kb_day1, kb_day2, kb_day3, kb_day4, kb_day5, kb_day6
from aiogram.dispatcher.filters import Text
from sql import users_register, reg_checker, qr_sender, asked, answered
from stateClasses import FeedbackState, answer,bot_ans
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from sql import callback_checker


bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
@dp.message_handler(Text(equals='Стоп'))
@dp.message_handler(Text(equals='На главный экран'))
async def start_comm(message: types.Message):
    if reg_checker(message.from_id):
        await bot.send_message(message.from_id, 'Добрый день, Вы попали в информационного бота "Школа фундаментальных технологий РБПО"!', reply_markup=kb_main_reg)
    else:
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


@dp.message_handler(Text(equals='2) Система управления базами данных'))
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
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Микроядерная операционная система KasperskyOS'))
async def day1_2(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Системы управления базами данных'))
async def day2_1(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Системы управления базами данных в "Linux"'))
async def day2_2(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Системы виртуализации и контейнеризации'))
async def day3_1(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Построение высоконагруженных сред'))
async def day3_2(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='JVM Internals'))
async def day4_1(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Интерпретатор Python'))
async def day4_2(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Системы сертификации СЗИ ФСТЭК России'))
async def day5_1(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Технологические центры безопасности ядра "Linux"'))
async def day5_2(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Композиционный анализ сторонних компонентов'))
async def day6_1(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Безопасность инфраструктур под управлением Kubernetes'))
async def day6_2(message: types.Message):
    await bot.send_message(message.from_id, 'Информация о лекции/спикере')


@dp.message_handler(Text(equals='Регистрация'))
async def register(message: types.Message):
    await bot.send_message(message.from_id, 'Ваша ссылка на регистрацию:\nhttps://forms.yandex.ru/u/65ba63fbeb61460b91183250/\nПосле регистрации можете получить свой qr код в разделе "Пропуска"')
    qr_name = qr_maker(message.from_id, 'test')
    users_register(message.from_id, 'test_day', qr_name)
    await bot.send_message(message.from_id, 'Добрый день, Вы попали в информационного бота "Школа фундаментальных технологий РБПО"!', reply_markup=kb_main_reg)


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
    await bot.send_message(message.from_id, 'Вы попали в раздел обратной связи', reply_markup=kb_feedback_aprove)



@dp.message_handler(Text(equals='Задать вопрос'))
async def callback_d(message: types.Message):
    await bot.send_message(message.from_id, 'Введите Ваш вопрос, наша группа поддержки оперативно ответит Вам!',
                           reply_markup=kb_feedback_aprove)
    await FeedbackState.take_quest.set()




@dp.message_handler(state=FeedbackState.take_quest)
async def feedback_sender(message: types.Message, state: FSMContext):
    mess = message.text
    text = f'''
✔Автор вопроса: @{message.from_user.username}


✔Телеграм id: {message.from_id}
✔Дата публикации вопроса: {data_maker()}

✔Вопрос: {mess}
    '''
    data= callback_checker(message.from_id)
    await bot.send_message(-1002007643494, text)
    mess_id = message.message_id
    await bot.send_message(message.from_id, 'Ваш вопрос отправлен!', reply_markup=kb_main)
    asked(message.from_id, mess, mess_id)
    await state.finish()


@dp.callback_query_handler()
async def callback_query_keyboard(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        mess_id = data['mess_id']
        print(mess_id)
    if callback_query.data == f'answer_{mess_id}':
        await bot.send_message(-1002007643494, 'Введите ответ:')
        await state
@dp.message_handler(Text(equals='Ответить'))
async def ans(mes:types.Message):
    await bot.send_message(mes.from_id,'Напишите Телеграм  Id')
    await bot_ans.user_id.set()

@dp.message_handler(state=bot_ans.user_id)
async def anss(mes:types.Message, state: FSMContext):
    await state.update_data(user_id=mes.text.lower())
    await bot.send_message(mes.from_id,'Напишите ответ')
    await bot_ans.next()

@dp.message_handler(state=bot_ans.ans)
async def anss(mes:types.Message,state:FSMContext):
    await state.update_data(ans=mes.text)
    await bot.send_message(mes.from_id,'Ответ отправлен')
    data = await state.get_data()
    id= str(data.get('user_id'))
    text = str(data.get('ans'))
    await bot.send_message(id,f'Ответ на ваш вопрос:\n{text}')
    await state.finish()

@dp.message_handler(state=answer.take_response)
async def response(message: types.Message):
    answered(message.from_id, message.text)
    await bot.send_message(message.from_id, 'Ответ отправлен!')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=100)