from urllib import request
from spamBot import spamBot
import requests as r
import random
import time
import json

id_copied_chat = input(f'Введите id чата откуда копировать сообщения: ')
id_insert_chat = input(f'Введите id чата куда копировать сообщения: ')
messages_count = int(input(f'Введите число сообщений кратное 100: '))
delay_start = int(input(f'Введите минимальную задержку на сервере: '))
delay_end = int(input(f'Введите максимальную задержку: '))
typing_delay = int(input(f'Введите задержку на печать: '))
response_delay = int(input(f'Введите задержку для ответа на предыдущее сообщение: '))


bot = spamBot(id_copied_chat, id_insert_chat)
tokens_list = open('tokens.txt', 'r', encoding='utf-8').read().splitlines()

# for token in tokens_list:
#     session = bot.create_session(token)
#     req = bot.send_join(session, "rTX2kXbD")
#     time.sleep(random.randint(2,10))

firs_session = bot.create_session(tokens_list[1])
loaded_msg = bot.get_messages(firs_session)

# with open('messages.json', 'w') as outfile:
#     json.dump(loaded_msg, outfile)

# print(loaded_msg)

all_messages = {}
all_messages.update(loaded_msg)
for i in range(0, (messages_count//100)):
    loaded_msg = bot.get_messages_before(firs_session, bot.get_last_messages_id(all_messages))
    all_messages.update(loaded_msg)

users_ids = []
for message in all_messages:
    if all_messages[message]['author_id'] not in  users_ids:
        users_ids.append(all_messages[message]['author_id'])

random.shuffle(users_ids)

sessions = {}
sessions_count = 0
for token in tokens_list:
    sessions[sessions_count] = {"token": bot.create_session(token), "users_ids": []}
    sessions_count += 1

session_id = 0
for ids in users_ids:
    sessions[session_id]['users_ids'].append(ids)
    session_id += 1
    if session_id == (len(sessions)):
        session_id = 0


loaded_msg = bot.reverseDict(all_messages)
sent_msg = {}
total_sent = 0
previous_sender = 0
for key in loaded_msg:
    previous_sender = loaded_msg[key]["author_id"]
    if loaded_msg[key]["author_id"] != previous_sender:
        delay_active = True
    else:
        delay_active = False
    try:
        msg = loaded_msg[key]
        print(f'Sending message: ' + msg["message_content"])
        delay = random.randint(delay_start, delay_end)
        if('https://' not in msg["message_content"] and ':' not in msg["message_content"] and '$' not in msg["message_content"]):
            for session in sessions:
                if loaded_msg[key]["author_id"] in sessions[session]['users_ids']:
                    bot.send_typing(sessions[session]['token'])
                    time.sleep(typing_delay)
                    req = bot.send_message(sessions[session]['token'], msg, sent_msg)
                    sent_msg[key] = {"msg_id": req["id"]}
                    previous_sender = loaded_msg[key]["author_id"]
                    total_sent += 1
        if(delay_active):
            print(f'Сообщение успешно отправлено (всего отправлено {total_sent}).')
            print(f'Перерыв {delay} секунд')
            time.sleep(delay)
        else:
            print(f'отвечает другой чеовек (всего отправлено {total_sent})')
            print(f'Перерыв {response_delay} секунд')
            time.sleep(response_delay)
    except Exception as e:
        print(f'Что-то пошло не так ERROR: {e.with_traceback}')
        time.sleep(20)