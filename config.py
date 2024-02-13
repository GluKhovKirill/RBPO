import os

# token = os.getenv("RBPO_BOT_TOKEN", "2141924201:AAEh3k3FJImHxjpUKV8U213hVvkJOnJD-WQ")
token = os.getenv("RBPO_BOT_TOKEN", "6507500673:AAHG-sKC_ext3DLS9k3a084b3HhnLEXM9tI")


host = os.getenv("MYSQL_IP", "localhost")
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "")
d_name = os.getenv("MYSQL_RBPO_DATABASE", "meetup")