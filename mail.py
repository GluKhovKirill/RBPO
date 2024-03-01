import smtplib
import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
from sql import mail_caught, mail_flag
from config import DAYS, password_mail, login
from threading import Timer
import datetime


def sender() -> bool:
    data, form_id = mail_caught()
    print('d', data, form_id)
    if not (data and form_id):
        return False
    name, otchestvo, mail, tg, days = data[0], data[1], data[2], data[3], data[4]

    days_substring = ""
    for day_n in sorted(days):
        days_substring += f' - {DAYS.get(day_n, "Не могу загрузить информацию...")}\n'

    tg_substring = "Пожалуйста, убедитесь, что вы активировали бота @RBPO_bot (отправили команду /start боту) и не заблокировали его!\nПропуска в виде QR-кодов будут отправлены через телеграм-бота и на почту."
    have_tg = bool(tg)

    text = f"""
{name} {otchestvo}!
Мы рады приветствовать Вас в Школе фундаментальных технологий РБПО!
Вы записались на следующие тематические дни:

{days_substring}

{tg_substring if have_tg else 'Пропуска в виде QR-кодов будут отправлены вам за сутки на данную почту.'}

Адрес: Малый Зал Дворца культуры МГТУ им. Н.Э. Баумана (Главный учебный корпус, над Домом Физики), 2-я Бауманская улица, 5с2 (схема прохода будет предоставлена позже)

Не забудьте взять с собой паспорт, если у вас нет пропуска на территорию МГТУ им. Н. Э. Баумана!

Ждем Вас!
—
С уважением, команда Школы фундаментальных технологий РБПО
secure-software.bmstu.ru
sdl-school@bmstu.ru
"""

    FROM = login
    context = ssl.create_default_context()
    try:
        with smtp.SMTP_SSL('mail.bmstu.ru', 465, context=context) as server:
            server.login(login, password_mail)

            msg = MIMEMultipart("alternative")
            msg["From"] = "sdl-school@bmstu.ru"  # FROM
            # set the receiver's email
            msg["To"] = mail
            # set the subject
            msg["Subject"] = "BMSTU RBPO SCHOOL"
            # set the text
            message = text
            msg.attach(MIMEText(message))

            server.sendmail(FROM, mail, msg.as_string())
            print("sent")
    except smtplib.SMTPDataError as err:
        print("mail sending error:", err)
        return None
    mail_flag(form_id)
    return True


def send_worker():
    print('send greeting mails')
    a = None
    try:
        a = sender()
        while a:
            a = sender()
    except Exception as err:
        a = None
        print("mailing critical", err)

    if a == None:
        print("set delay 15 min")
        delay: int = 15 * 60
    else:
        delay: int = get_secs_till_six()
    print(f'next in {delay} secs')
    t = Timer(delay, send_worker)
    t.start()


def start_sender() -> None:
    t = Timer(5, send_worker)
    t.start()


# send_worker()

def get_secs_till_six(target_hour=6, target_minute=0) -> int:
    now = datetime.datetime.now()
    if now.hour >= target_hour:  # or (target_minute<now.minute and now.hour==target_minute):
        temp = now + datetime.timedelta(days=1)
    else:
        temp = now
    target = datetime.datetime(year=temp.year, month=temp.month, day=temp.day, hour=target_hour, minute=0, second=0)

    return (target - datetime.datetime.now()).seconds

# print()
#
