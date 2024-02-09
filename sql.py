import pymysql
from config import host, user, password, d_name


def create_db():
    con = pymysql.connect(host=host, user=user, password=password)
    with con:
        cur = con.cursor()
        try:
            cur.execute(f'CREATE DATABASE {d_name}')
            con.commit()
        except:
            print('Database is exist')


def users_register(tg_id, day, qr):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO `main`(`tg_id`, `day`, `qr`) VALUES ("{tg_id}", "{day}", "{qr}")')
        con.commit()


def reg_checker(tg_id):
    flag = False
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'SELECT `tg_id` FROM `main`')
        data = cur.fetchall()
        for i in data:
            if i[0] == tg_id:
                flag = True
    return flag


def qr_sender(tg_id):
    a = []
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'SELECT `qr` FROM `main` WHERE `tg_id` = {tg_id}')
        data = cur.fetchall()
        for i in data:
            if i[0] and i[0] != 'None':
                a.append(i[0])
    return a


def asked(tg_id, quest):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO `feedback`(`asked`, `quest`) VALUES ("{tg_id}","{quest}")')
        con.commit()


# UPDATE `feedback` SET `answered`='ddsds', `ans_text`='ответ' WHERE `asked` = tg_id AND `answered` IS NULL;

def answered(tg_id, ans):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(
            f'UPDATE `feedback` SET `answered`="{tg_id}", `ans_text`="{ans}" WHERE `asked` = tg_id AND `answered` IS NULL')
        con.commit()


def callback_checker(tg_id):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(
            f'SELECT `mess_id` FROM `feedback` WHERE `asked` = {tg_id}')
        data = cur.fetchall()
    return data[-1][0]


def create_table_feedback():
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                f"CREATE TABLE feedback (`uid` INT NOT NULL AUTO_INCREMENT, `mess_id` BIGINT NULL, `asked` TEXT NULL, `quest` TEXT NULL, PRIMARY KEY (`uid`))")
        except:
            print('Table is exist')


def create_table_main():
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                f"CREATE TABLE main (`uid` INT NOT NULL AUTO_INCREMENT, `tg_id` BIGINT NOT NULL, `day` TEXT NOT NULL, `qr` TEXT NOT NULL, PRIMARY KEY (`uid`))")
        except:
            print('Table is exist')


def create_table_admins():
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                f"CREATE TABLE admins (`uid` INT NOT NULL AUTO_INCREMENT, `tg_id` BIGINT NOT NULL, PRIMARY KEY (`uid`))")
        except:
            print('Table is exist')


def create_table_from_gmail():
        con = pymysql.connect(host=host, user=user, password=password, database=d_name)
        with con:
            cur = con.cursor()
            try:
                cur.execute(
                    f"CREATE TABLE from_gmail (`uid` INT NOT NULL AUTO_INCREMENT, `form_id` BIGINT NOT NULL, `surname` TEXT NOT NULL, `name` TEXT NOT NULL, `otchestvo` TEXT NOT NULL, `day` TEXT NOT NULL, `org` TEXT NOT NULL, `mail` TEXT NOT NULL, `tg` TEXT NOT NULL, PRIMARY KEY (`uid`))")
            except:
                print('Table is exist')


def create_table_questions():
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                f"CREATE TABLE questions (`uid` INT NOT NULL AUTO_INCREMENT, `tg_id` BIGINT NOT NULL, `quest` TEXT NOT NULL, `status` TINYINT NULL, `answer` TEXT  NULL, PRIMARY KEY (`uid`))")
        except:
            print('Table is exist')


def admin_catcher():
    adm_list = []
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT `tg_id` FROM `admins`")
        f = cur.fetchall()
    for adm in f:
        adm_list.append(adm[0])
    return adm_list


def quest_insert(mess, tg_id):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO `questions`(`tg_id`, `quest`) VALUES ("{tg_id}", "{mess}")')
        con.commit()


def answer_caughter():
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'SELECT * FROM `questions` WHERE `status` is NULL')
        quest = cur.fetchone()
        user_quest = {'tg_id': quest[1], 'quest': quest[2], 'uid': quest[0]}
    return user_quest


def answer_collect(uid, ans):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"UPDATE `questions` SET `status`= TRUE,`answer`='{ans}' WHERE `uid` = {uid};")
        con.commit()


def gmail_catcher(form_id, surname, name, otchestvo, day, org, mail, tg):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO `from_gmail`(`form_id`, `surname`, `name`, `otchestvo`, `day`, `org`, `mail`, `tg`) VALUES ('{form_id}','{surname}','{name}','{otchestvo}','{day}','{org}','{mail}','{tg}')")
        con.commit()


def take_gmail_user(username):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    days = []
    with con:
        cur = con.cursor()
        try:
            cur.execute(f'SELECT `day` FROM `from_gmail` WHERE `tg` = "{username}"')
            data = cur.fetchall()
            for i in data:
                days.append(i[0])
        except:
            days = []
    return days

