#!/usr/bin/python3
print()
from telegram.client import Telegram
import cgi
import time

API_ID = 15624617
API_HASH = '8875f18d64f3cbffac3009a0bcc5e2bc'

def send():
    # Парсер передаваемых параметров
    args = cgi.parse()
    PHONE_FROM = args['phone_from'][0]
    PHONE_TO = args['phone_to'][0]
    MESSAGE = args['message'][0]

    target_user_id = ''
    tg = Telegram(
        api_id=API_ID,
        api_hash=API_HASH,
        phone=PHONE_FROM,
        database_encryption_key='',
        tdlib_verbosity=7,
        library_path='/usr/local/lib/python3.8/dist-packages/td/tdlib/lib/libtdjson.so.1.8.4'
    )

    tg.login()

    # Получаем user_id контактов отправителя и ищем среди них адресата по номеру телефона.
    contacts = tg.call_method('getContacts', {'': ''})
    contacts.wait()

    if contacts.update['user_ids']:
        for c in contacts.update['user_ids']:
            user = tg.get_user(c)
            user.wait()
            if user.update['phone_number']:
                if user.update['phone_number'] == PHONE_TO:
                    target_user_id = c
                    break

    # Если не нашли среди контактов - создаем новый контакт.
    # Взамен получаем user_id.
    if not target_user_id:
        new_contacts = [{'@type': 'contact', 'phone_number': PHONE_TO}]
        new_user = tg.call_method('importContacts', {'contacts': new_contacts})
        new_user.wait()
        if new_user.update['user_ids'][0] > 0:
            target_user_id = new_user.update['user_ids'][0]

    # Создаем новый приватный чат и получаем его chat_id ИЛИ получаем chat_id уже существующего.
    if target_user_id:
        chat_id = tg.call_method('createPrivateChat', {'user_id': target_user_id})
        chat_id.wait()

    chats = tg.call_method('getChats', {'': ''})
    chats.wait()

    if chat_id.update['id']:

        #Отправка текста
        input_param = {'chat_id': chat_id.update['id'],
                      'input_message_content':
                          {'@type': 'inputMessageText',
                           'text': {'@type': 'formattedText',
                                    'text': MESSAGE}
                           }
                       }

        result = tg.call_method('sendMessage', input_param)
        result.wait()

        if result.error:
            print(f'-2\n{result.error_info}\r', end='')
        else:
            print(f'1\n{result.update["id"]}##SEP##{result.update["date"]}\r', end='')
    time.sleep(2)
    tg.stop()


send()
