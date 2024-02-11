import os
from amzqr import amzqr
import imaplib
import email
import base64
from bs4 import BeautifulSoup
import json
from sql import gmail_catcher
from threading import Timer


MAIL_CHECK_TIMER = None
MAIL_CHECK_DELAY = 30
def qr_maker(tg_id, day):
    name = f'qr_{tg_id}.png'
    version, level, qr_name = amzqr.run(
        words=f'{day}/{tg_id}',
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


