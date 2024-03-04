import os
from amzqr import amzqr
import imaplib
import email
import base64
from bs4 import BeautifulSoup
import json
from sql import gmail_catcher
from threading import Timer
from sql import quest_checker, sql_tg_id_catcher, sql_uid_cather


MAIL_CHECK_TIMER = None
MAIL_CHECK_DELAY = 30
DB_CHECK_TIMER = None
DB_CHECK_DELAY = 5
def qr_maker(tg_id, day):
    name = f'qr_{tg_id}.png'
    version, level, qr_name = amzqr.run(
        words=f'',
        version=1,
        level='H',
        picture='qr_codes/bg.jpg',
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=f'qr_codes/{name}',
        save_dir=os.getcwd()
    )
    return name


def from_gmail_catcher():
    print("Checking mail for forms")
    global MAIL_CHECK_TIMER
    if MAIL_CHECK_TIMER:
        MAIL_CHECK_TIMER.cancel()
        MAIL_CHECK_TIMER = None
    list_g = []
    mail_pass = "spku kxbv suwv rwel"
    username = "pochtapeckinbmstu@gmail.com"
    imap_server = "imap.gmail.com"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, mail_pass)
    imap.select("INBOX")
    for i in imap.uid('search', "UNSEEN", "ALL")[1][0].split():
        res, msg = imap.uid('fetch', i, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        for part in msg.walk():
            if part.get_content_maintype() == 'text':
                data = base64.b64decode(part.get_payload()).decode()
                soup = BeautifulSoup(data, 'html.parser')
                info = list(filter(lambda x: x and 'созданный пользователем Yandex Forms. Яндекс не несёт' not in x,
                                   map(lambda x: x.strip(), soup.find('pre').text.split('\n'))))
                form_id = info[0]
                form_data = json.loads(info[1])
                tg_id = form_data.get('Ваш Telegram', '').strip().lstrip('@')
                for i in filter(lambda x: x and x.strip(), form_data['Какие дни вы планируете посетить?'].split('День')):
                    gmail_catcher(form_id.strip(), form_data.get('Фамилия','').strip(), form_data.get('Имя', '').strip(), form_data.get('Отчество', '').strip(), i.strip(), form_data.get('Учебная группа / Организация', '').strip(), form_data.get('Ваша почта', '').strip(), tg_id)
    MAIL_CHECK_TIMER = Timer(MAIL_CHECK_DELAY, from_gmail_catcher)
    MAIL_CHECK_TIMER.start()


def quest_frame_checker():
    data = quest_checker()
    global DB_CHECK_TIMER
    if DB_CHECK_TIMER:
        DB_CHECK_TIMER.cancel()
    if data != 0:
        return f'Подъехали новые вопросы: {data}\nПора отвечать❗'

    DB_CHECK_TIMER = Timer(DB_CHECK_DELAY, quest_frame_checker)
    DB_CHECK_TIMER.start()


def uid_generator():
    ans=[]
    all_data = sql_uid_cather()
    for data in all_data:
        url_code = base64.b64encode((f"{data[0]}_1").encode("UTF-8"))
        final_code = str(url_code).split("'")[1].strip("==")
        username = data[4]
        mess = f"""
{data[2]} {data[3]}, напоминаем Вам, что завтра пройдут первые лекции по фундаментальным информационным технологиям, их развитию в России и в мире « (https://secure-software.bmstu.ru/)Школа фундаментальных технологий РБПО (https://secure-software.bmstu.ru/)» (https://secure-software.bmstu.ru/)💛

https://secure-software.bmstu.ru/confirm.html?register=remote&uid={final_code}
https://rbpo-school-validation.tw1.ru:1830/visited?uid={final_code}

📍 Где? 
Малый Зал ЦКИ (ГУК, над Домом Физики)

📍 Программа дня:

«Операционные системы на основе ядра Linux: сообщество, дистрибутив, жизненный цикл». 
⏲11:00 - 13:00
👥Спикер: Георгий Курячий, ведущий разработчик ОС «Альт» (https://www.basealt.ru/) и преподаватель факультета вычислительной математики и кибернетики (ВМК) МГУ.😀
🔔 Анонс

❗️Кофе-брейк: 13:00-13:30

«Микроядерные операционные системы. Summa technologiae». 
⏲13:30 - 15:30
👥Спикеры: Сергей Рогачев,
руководитель отдела разработки безопасной платформы, и широко известный в сообществе Дмитрий Шмойлов, руководитель отдела безопасности программных продуктов «Лаборатории Касперского» (https://os.kaspersky.ru/development/)        
        
"""
        tg_id = sql_tg_id_catcher(username)
        if tg_id == None:
            continue
        else:
            tg_id = tg_id[0]

        user = {"tg_id": tg_id, "mess": mess,
                "mail": "kirill.gluhov2003@yandex.ru"}
        ans.append(user)

    return ans

# print(uid_generator())


