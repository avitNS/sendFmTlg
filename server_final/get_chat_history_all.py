#!/usr/bin/python3
print()
from telegram.client import Telegram
import cgi

API_ID = 15624617
API_HASH = '8875f18d64f3cbffac3009a0bcc5e2bc'

def get_chat_history():
    # Парсер передаваемых параметров
    args = cgi.parse()
    PHONE_FROM = args['phone_from'][0]
    PHONE_TO = args['phone_to'][0]
    TARGET_COUNT = args['target_count'][0]


    target_user_id = ''
    tg = Telegram(
        api_id=API_ID,
        api_hash=API_HASH,
        phone=PHONE_FROM,
        database_encryption_key='',
        tdlib_verbosity=2,
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

    messages_list_result = ''
    last_id =''
    target_count = int(TARGET_COUNT) - 1

    if chat_id.update['id']:

        # Находим последнее сообщение чата
        last_message_id = tg.call_method('getChatHistory', {
            'chat_id': chat_id.update['id'],
            'from_message_id': 0,
            'offset': 0,
            'limit': 100,
            'only_local': False
        })
        last_message_id.wait()
        last_id = last_message_id.update['messages'][0]['id']

        id_msg = last_message_id.update['messages'][0]['id']
        type_msg = last_message_id.update['messages'][0]['content']['@type']
        date_msg = last_message_id.update['messages'][0]['date']
        is_out_msg = last_message_id.update['messages'][0]['is_outgoing']
        content_msg = ''

        if type_msg == 'messageText':
            content_msg = last_message_id.update['messages'][0]['content']['text']['text']
        elif type_msg == 'messageSticker':
            content_msg = last_message_id.update['messages'][0]['content']['sticker']['emoji']
        elif type_msg == 'messageAnimatedEmoji':
            content_msg = last_message_id.update['messages'][0]['content']['animated_emoji']['sticker']['emoji']
        elif type_msg == 'messageDocument':
            content_msg = last_message_id.update['messages'][0]['content']['document']['file_name']
        elif type_msg == 'messagePhoto':
            content_msg = 'Фото'
        elif type_msg == 'messageVoiceNote':
            content_msg = 'Голосовое сообщение'
        elif type_msg == 'messageCall':
            content_msg = 'Звонок'
        if content_msg:
            messages_list_result += f"{id_msg}#SEP#{type_msg}#SEP#{date_msg}#SEP#{is_out_msg}#SEP#{content_msg}#ETR#"

        while target_count > 0:

            last_messages = tg.call_method('getChatHistory', {
                'chat_id': chat_id.update['id'],
                'from_message_id': last_id,
                'offset': 0,
                'limit': target_count,
                'only_local': False
            })
            last_messages.wait()

            if len(last_messages.update['messages']) == 0 or \
                    last_messages.update == 'None' or \
                    not last_messages.update or \
                    last_messages.update['total_count'] == 0:
                break

            if last_id == last_messages.update['messages'][-1]['id']:
                break

            total_count = last_messages.update['total_count']
            target_count = target_count - total_count
            last_id = last_messages.update['messages'][-1]['id']

            for message in last_messages.update['messages']:
                id_msg = message['id']
                type_msg = message['content']['@type']
                date_msg = message['date']
                is_out_msg = message['is_outgoing']
                content_msg = ''

                if type_msg == 'messageText':
                    content_msg = message['content']['text']['text']
                elif type_msg == 'messageSticker':
                    content_msg = message['content']['sticker']['emoji']
                elif type_msg == 'messageAnimatedEmoji':
                    content_msg = message['content']['animated_emoji']['sticker']['emoji']
                elif type_msg == 'messageDocument':
                    content_msg = message['content']['document']['file_name']
                elif type_msg == 'messagePhoto':
                    content_msg = 'Фото'
                elif type_msg == 'messageVoiceNote':
                    content_msg = 'Голосовое сообщение'
                elif type_msg == 'messageCall':
                    content_msg = 'Звонок'
                if content_msg:
                    messages_list_result += f"{id_msg}#SEP#{type_msg}#SEP#{date_msg}#SEP#{is_out_msg}#SEP#{content_msg}#ETR#"

    print(messages_list_result)
    tg.stop()


get_chat_history()