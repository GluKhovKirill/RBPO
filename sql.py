import pymysql
from adaptix import Retort
from config import host, user, password, d_name, DAY_N
import dataclasses


@dataclasses.dataclass
class USER:
    uid: str
    form_id: str
    surname: str
    name: str
    otchestvo: str
    day: str
    org: str
    mail: str
    tg: str


def create_db():
    con = pymysql.connect(host=host, user=user, password=password)
    with con:
        cur = con.cursor()
        try:
            cur.execute(f'CREATE DATABASE {d_name}')
            con.commit()
        except:
            print('Database is exist')


def users_register(tg_id, username):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'SELECT  `tg_id`, `username` FROM `main`')
        data = cur.fetchall()
        for i in data:
            if tg_id == i[0] and username == i[1]:
                return
        username = username.strip().lstrip('@')
        cur.execute(f'INSERT INTO `main`(`tg_id`, `username`) VALUES ("{tg_id}", "{username}")')
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
                f"CREATE TABLE main (`uid` INT NOT NULL AUTO_INCREMENT, `tg_id` BIGINT NOT NULL,`username` TEXT NOT NULL, `qr` TEXT NOT NULL, PRIMARY KEY (`uid`))")
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
                f"CREATE TABLE from_gmail (`uid` INT NOT NULL AUTO_INCREMENT, `form_id` BIGINT NOT NULL, `surname` TEXT NOT NULL, `name` TEXT NOT NULL, `otchestvo` TEXT NOT NULL, `day` TEXT NOT NULL, `org` TEXT NOT NULL, `mail` TEXT NOT NULL, `tg` TEXT NOT NULL, `flag` , `flag_tg` TINYINT NULL, PRIMARY KEY (`uid`))")
        except:
            print('Table is exist')


def create_table_questions():
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        try:
            cur.execute(
                f"CREATE TABLE questions (`uid` INT NOT NULL AUTO_INCREMENT, `tg_id` BIGINT NOT NULL, `quest` TEXT NOT NULL, `status` TINYINT NULL, `answer` TEXT  NULL, `temp_ans` BIGINT NULL, PRIMARY KEY (`uid`))")
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


def answer_caughter(tg_id):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'SELECT * FROM `questions` WHERE `status` is NULL')
        quests = cur.fetchall()
        for i in quests:
            if i[-1] == tg_id or i[-1] == None:
                user_quest = {'tg_id': i[1], 'quest': i[2], 'uid': i[0], 'temp': i[-1]}
                cur.execute(f"UPDATE `questions` SET `temp_ans`= {tg_id} WHERE `uid` = {i[0]} and `temp_ans` is NULL")
                con.commit()
                return user_quest, user_quest['temp']


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
        cur.execute(
            f"INSERT INTO `from_gmail`(`form_id`, `surname`, `name`, `otchestvo`, `day`, `org`, `mail`, `tg`) VALUES ('{form_id}','{surname}','{name}','{otchestvo}','{day}','{org}','{mail}','{tg}')")
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


def quest_checker():
    counter = 0
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT `uid`FROM `questions` WHERE `status` is NULL and `temp_ans` is NULL")
        dataframe = cur.fetchall()
        for i in dataframe:
            counter += 1
    return counter


def unloading(tg_id):
    all_data = []
    retort = Retort()
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM `from_gmail`")
        data = cur.fetchall()
    for i in data:
        processed_persons: list[USER] = []
        processed_persons.append(USER(
            uid=i[0],
            form_id=i[1],
            surname=i[2],
            name=i[3],
            otchestvo=i[4],
            day=i[5],
            org=i[6],
            mail=i[7],
            tg=i[8]
        )
        )
        all_data.append(dict(reversed(list(retort.dump(processed_persons[0], USER).items()))))

    with open(f'unload/unload_{tg_id}.csv', 'w', encoding='utf-8') as f:
        f.write("uid;form_id;surname;name;otchestvo;day;org;mail;tg\n")
        for i in all_data:
            f.write(
                f"{i.get('uid')};{i.get('form_id')};{i.get('surname')};{i.get('name')};{i.get('otchestvo')};{i.get('day')};{i.get('org')};{i.get('mail')};{i.get('tg')}\n")


def mail_caught():
    data = []
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'SELECT `form_id` FROM `from_gmail` WHERE `flag` is NULL group by `form_id`')
        id = cur.fetchone()
        if not id:
            return None, None
        id = id[0]
        cur.execute(f"SELECT `name`, `otchestvo`, `day`, `mail`, `tg` FROM `from_gmail` WHERE `form_id` = {id}")
        datas = cur.fetchall()
        name, otchestvo, mail, tg = None, None, None, None
        days = set()
        for j in datas:
            t = [i for i in j]
            if t[4]:
                tg = t[4].lstrip('https://t.me/')
            else:
                tg = ""
            otchestvo = t[1]
            name = t[0]
            mail = t[3]
            data.append(t)
            days.add(int(t[2].split('.')[0]))
        folk = [name, otchestvo, mail, tg, sorted(days)]
    return folk, id


def mail_flag(form_id):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"UPDATE `from_gmail` SET `flag`= 1 WHERE `form_id` = {form_id}")
        con.commit()


def get_tg_valid_users():
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT `tg_id`,`username` FROM `main` WHERE `username` is NOT NULL;")
        data = cur.fetchall()
    return data


def get_data_by_alias(tg_alias: str):
    #
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(
            f"""SELECT name,otchestvo,day FROM `from_gmail` WHERE (tg = "{tg_alias}" or tg = "@{tg_alias}") AND (`flag_tg` IS NULL);""")
        data = cur.fetchall()
    return data


def db_update(username):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"UPDATE `from_gmail` SET `flag_tg`= 1 WHERE `tg` = '{username}'")
        con.commit()


def qr_uid_finder(username: str):
    uname_lower = username.strip().lower()
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT `uid` FROM `from_gmail` WHERE day like '{DAY_N}.%' and LOWER(`tg`) = '{uname_lower}'")
        data = cur.fetchone()
        if data: data = data[0]
    return data
