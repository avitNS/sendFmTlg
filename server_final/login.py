#!/usr/bin/python3
print()
from telegram.client import Telegram
import cgi

API_ID = 15624617
API_HASH = '8875f18d64f3cbffac3009a0bcc5e2bc'

def login():
    args = cgi.parse()
    PHONE_FROM = args['phone_from'][0]
    CODE = args['code'][0]

    tg = Telegram(
        api_id=API_ID,
        api_hash=API_HASH,
        phone=PHONE_FROM,
        database_encryption_key='',
        library_path='/usr/local/lib/python3.8/dist-packages/td/tdlib/lib/libtdjson.so.1.8.4'
    )

    while not tg.authorization_state:
        tg.login(blocking=False)
    print(tg.authorization_state)
    if CODE:
        tg.send_code(CODE)
        print(tg.authorization_state)

    tg.stop()

login()
