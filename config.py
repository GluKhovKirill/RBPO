import os

# token = os.getenv("RBPO_BOT_TOKEN", "2141924201:AAEh3k3FJImHxjpUKV8U213hVvkJOnJD-WQ")
token = os.getenv("RBPO_BOT_TOKEN", "6507500673:AAHG-sKC_ext3DLS9k3a084b3HhnLEXM9tI")

host = os.getenv("MYSQL_IP", "localhost")
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "")
d_name = os.getenv("MYSQL_RBPO_DATABASE", "meetup")
DAYS = {
    1: 'День 1. Операционные системы (5 марта (вторник) 11:00 - 15.30 )',
    2: 'День 2. СУБД',
    3: 'День 3. Виртуализация и контейнеризация',
    4: 'День 4. Интерпретаторы',
    5: 'День 5. РБПО',
    6: 'День 6. Композиционный и компонентный анализ'
}

login = os.getenv("mail_login","")
password_mail = os.getenv("mail_pass","")
DAY_N = 4