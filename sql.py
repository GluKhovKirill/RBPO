import pymysql
from config import host, user, password, d_name

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


def asked(tg_id, quest, mess_id):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'INSERT INTO `feedback`(`asked`, `quest`, `mess_id`) VALUES ("{tg_id}","{quest}", "{mess_id}")')
        con.commit()


#UPDATE `feedback` SET `answered`='ddsds', `ans_text`='ответ' WHERE `asked` = tg_id AND `answered` IS NULL;

def answered(tg_id, ans):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(f'UPDATE `feedback` SET `answered`="{tg_id}", `ans_text`="{ans}" WHERE `asked` = tg_id AND `answered` IS NULL')
        con.commit()


def callback_checker(tg_id):
    con = pymysql.connect(host=host, user=user, password=password, database=d_name)
    with con:
        cur = con.cursor()
        cur.execute(
            f'SELECT `mess_id` FROM `feedback` WHERE `asked` = {tg_id}')
        data = cur.fetchall()
    return data[-1][0]

