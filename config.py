import os

token = os.getenv("RBPO_BOT_TOKEN", "2141924201:AAEh3k3FJImHxjpUKV8U213hVvkJOnJD-WQ")


host = os.getenv("MYSQL_IP", "localhost")
user = os.getenv("MYSQL_USER", "root")
password = os.getenv("MYSQL_PASSWORD", "")
d_name = os.getenv("MYSQL_RBPO_DATABASE", "meetup")