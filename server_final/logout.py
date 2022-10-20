#!/usr/bin/python3
print()
from telegram.client import Telegram
import cgi


API_ID = 15624617
API_HASH = '8875f18d64f3cbffac3009a0bcc5e2bc'


def logout():
    args = cgi.parse()
    PHONE_FROM = args['phone_from'][0]

    tg = Telegram(
        api_id=API_ID,
        api_hash=API_HASH,
        phone=PHONE_FROM,
        database_encryption_key='',
        library_path='/usr/local/lib/python3.8/dist-packages/td/tdlib/lib/libtdjson.so.1.8.4'
    )

    tg.login()
    tg.call_method('logOut', {'': ''})
    tg.stop()


logout()
