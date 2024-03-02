import asyncio

import aiogram.utils.exceptions
import logging
from sql import get_tg_valid_users, get_data_by_alias, db_update
from config import DAYS
# import asgiref.sync
# from threading import Timer



# @asgiref.sync.async_to_sync
async def notify(bot):
    for uid, tg_alias in get_tg_valid_users():
        # tg_alias from from_gmail
        # SELECT name,otchestvo,day FROM `from_gmail` WHERE tg = "{tg_alias}" or tg = "@{tg_alias}";
        user_data = get_data_by_alias(tg_alias)
        if not user_data:
            continue
        name = user_data[0][0]
        otchestvo = user_data[0][1]
        days = [int(i[2].lower().strip().strip("день").split(".")[0]) for i in user_data]

        days_substring = ""
        for day_n in sorted(days):
            days_substring += f' - 🗓<u>{DAYS.get(day_n, "Не могу загрузить информацию...")}</u>\n'

        text = f"""
😎 <i>{name} {otchestvo}</i>!

Вы записались на следующие тематические дни:

{days_substring}

🗺Адрес: <a href="https://yandex.ru/maps/-/CDFBAA8-"><b>Малый Зал Дворца культуры МГТУ им. Н.Э. Баумана (Главный учебный корпус, над Домом Физики), 2-я Бауманская улица, 5с2</b></a> (схема прохода будет предоставлена позже)

❗️<b><u>Не забудьте взять с собой паспорт, если у вас нет пропуска на территорию МГТУ им. Н. Э. Баумана!</u></b>

🕐 Бот вышлет Вам QR-код для прохода на лекцию за сутки до мероприятия

Ждем Вас!
""".strip()
        # print(uid, text,sep='\n')
        logging.info(f"Sending to {uid} ({tg_alias})")
        try:
            await bot.send_message(uid, text, parse_mode="HTML")
            db_update(tg_alias)
        except aiogram.utils.exceptions.ChatNotFound:
            logging.warning(f"Чат не найден:  {uid} ({tg_alias})")
        except aiogram.utils.exceptions.BotBlocked:
            logging.error(f"Чел заблочил бота:  {uid} ({tg_alias})")
        except Exception as err:
            logging.critical("Дичь при отправке", err)
        # await bot.send_location(uid, 55.767017, 37.684634)


async def start_notifier(bot):
    while True:
        try:
            await notify(bot)
        except Exception as err:
            logging.critical("Нотифаер тг ругается:",err)
        finally:
            await asyncio.sleep(20)
    #t = Timer(20, start_notifier, [bot])
    #t.start()