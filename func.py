import os
from amzqr import amzqr
from datetime import datetime


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

qr_maker(313113, 'ddd')

def data_maker():
    now = datetime.now()
    date_time = now.strftime("%m.%d.%Y, %H:%M:%S")
    return date_time


