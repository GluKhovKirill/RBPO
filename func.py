import os
import ssl
import smtplib
import smtplib as smtp
from amzqr import amzqr
import imaplib
import email
import base64
from bs4 import BeautifulSoup
import json
from sql import gmail_catcher
from threading import Timer
from sql import quest_checker, sql_tg_id_catcher, sql_uid_cather
from config import DAYS, password_mail, login
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import time



MAIL_CHECK_TIMER = None
MAIL_CHECK_DELAY = 30
DB_CHECK_TIMER = None
DB_CHECK_DELAY = 5
def qr_maker(tg_id):
    name = f'qr_{tg_id}.png'
    version, level, qr_name = amzqr.run(
        words=f'{tg_id}',
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
        mail = data[5]
        qr_fname = qr_maker(final_code)
        mess = f"""
{data[2]} {data[3]}, напоминаем Вам, что завтра пройдут первые лекции по фундаментальным информационным технологиям, их развитию в России и в мире «Школы фундаментальных технологий РБПО»

Если Вы планируете присутствовать очно, перейдите по ссылке (QR-код для входа приложен к сообщению):
https://secure-software.bmstu.ru/confirm.html?register=real&uid={final_code}

Если Вы планируете смотреть лекцию удаленно:
https://secure-software.bmstu.ru/confirm.html?register=remote&uid={final_code}


📍 Где? 
Малый Зал Дворца культуры (МЗДК) МГТУ им. Н.Э. Баумана (Главный учебный корпус, над Домом Физики), 2-я Бауманская улица, 5с2 (ниже приложены схемы прохода)

📍 Программа дня:

«Операционные системы на основе ядра Linux: сообщество, дистрибутив, жизненный цикл». 
⏲11:00 - 13:00
👥Спикер: Георгий Курячий, ведущий разработчик ОС «Альт» и преподаватель факультета вычислительной математики и кибернетики (ВМК) МГУ.


❗️Кофе-брейк: 13:00-13:30

«Микроядерные операционные системы. Summa technologiae». 
⏲13:30 - 15:30
👥Спикеры: Сергей Рогачев, руководитель отдела разработки безопасной платформы

Дмитрий Шмойлов, руководитель отдела безопасности программных продуктов «Лаборатории Касперского».        

️️️❗Не забудьте взять с собой паспорт, если у вас нет пропуска на территорию МГТУ им. Н. Э. Баумана!

️️️❗Крайне рекомендуем прибывать минимум за пол часа до начала мероприятия из-за длительности оформления оформления прохода на территорию университета!

️️️❗Ссылка на онлайн-трансляцию: https://rutube.ru/channel/35564652/about/
        
"""
        tg_id = sql_tg_id_catcher(username)
        if tg_id == None:
            continue
        else:
            tg_id = tg_id[0]

        user = {"tg_id": tg_id, "mess": mess,
                "mail": mail,
                "qr": qr_fname}
        while True:
            try:
                sender(mess, mail, qr_fname)
                print("sent 2",mail)
                break
            except Exception as err:
                print("ERR", err)
                time.sleep(16*60)


    return ans





def sender(mess, mail, qr_fname) -> bool:

    days_substring = ""

    text = mess

    FROM = login
    context = ssl.create_default_context()
    try:
        with smtp.SMTP_SSL('mail.bmstu.ru', 465, context=context) as server:
            server.login(login, password_mail)

            with open('entry1.jpg', 'rb') as f:
                img_data1 = f.read()

            with open('entry2.jpg', 'rb') as f:
                img_data2 = f.read()

            with open('qr_codes/'+qr_fname, 'rb') as f:
                img_data3 = f.read()



            msg = MIMEMultipart("related")

            msg_image = MIMEImage(img_data1)
            msg_image.add_header('Content-ID', 'map_1.png')
            msg.attach(msg_image)

            msg_image2 = MIMEImage(img_data2)
            msg_image2.add_header('Content-ID', 'map_2.png')
            msg.attach(msg_image2)

            msg_image3 = MIMEImage(img_data3)
            msg_image3.add_header('Content-ID', 'qr.png')
            msg.attach(msg_image3)

            # image1 = MIMEImage(img_data1, name=os.path.basename('entry1.jpg'))
            # msg.attach(image1)
            # image2 = MIMEImage(img_data2, name=os.path.basename('entry2.jpg'))
            # msg.attach(image2)
            # image3 = MIMEImage(img_data3, name=os.path.basename('entry3.jpg'))
            # msg.attach(image3)
            msg["From"] = "sdl-school@bmstu.ru"  # FROM
            # set the receiver's email
            msg["To"] = mail
            # set the subject
            msg["Subject"] = "BMSTU RBPO SCHOOL"
            # set the text
            message = text
            msg.attach(MIMEText(message))

            server.sendmail(FROM, mail, msg.as_string())
            # print("sent")
    except smtplib.SMTPDataError as err:
        print("mail sending error:", err)
        return None
    return True

if __name__ == "__main__":
    uid_generator()
# >>>>>>> Stashed changes
