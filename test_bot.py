from aiogram import Bot, Dispatcher, types, executor
from config import token
from func import uid_generator
import asgiref.sync
bot = Bot(token=token)
dp = Dispatcher(bot)

# print(uid_generator())
# @asgiref.sync.async_to_sync
@dp.message_handler(commands=['secret'])
async def send_tg(message):
    await bot.send_message(message.from_id,"go")
    for i in uid_generator():
        tg_id = i["tg_id"]
        msg = i["mess"]
        if tg_id != 403054226:
            continue
        print("sent 2", tg_id)
        await bot.send_message(tg_id,msg)
# send_tg()
executor.start_polling(dp, skip_updates=True, timeout=20)