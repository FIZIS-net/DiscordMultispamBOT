from spamBot import spamBot
import requests as r
import random
import time
# first_discord_token = input(f'Введите токен первого аккаунта: ')
# second_discord_token = input(f'Введите токен первого аккаунта: ')
# id_copied_chat = input(f'Введите id чата откуда копировать сообщения: ')
# id_insert_chat = input(f'Введите id чата куда копировать сообщения: ')
# messages_count = int(input(f'Введите число сообщений кратное 100: '))
# dlay_start = int(input(f'Введите от скольки секунд делать задержку: '))
# delay_end = int(input(f'Введите до скольки секунд делать задержку: '))

bot = spamBot(919946959949795412, 932974315954114583)
tokens_list = open('tokens.txt', 'r', encoding='utf-8').read().splitlines()



firs_session = bot.create_session('OTMxNzE5NjQ0OTMzNDEwODI2.YeIh6A.CRTlv--PjA52RlTEeEbfslnqrt0')
second_session = bot.create_session('OTMxNzM3NzcwMzAzNTc0MDU2.YeIy1A.y8-SmcXAU_kjWliafFKjnHXBcEc')

loaded_msg = bot.get_messages(firs_session)
all_messages = {}
all_messages.update(loaded_msg)

for i in range(0, (1000//100)):
    loaded_msg = bot.get_messages_before(firs_session, bot.get_last_messages_id(all_messages))
    all_messages.update(loaded_msg)

users_ids = []
for message in all_messages:
    if all_messages[message]['author_id'] not in  users_ids:
        users_ids.append(all_messages[message]['author_id'])
print(users_ids)
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
total_sent = 0

for key in loaded_msg:
    try:
        msg= loaded_msg[key]["message_content"]
        print(f'Sending message {msg}')
        _data = {'content':msg, 'tts':False}
        delay = random.randint(1, 3)
        if('https://' not in msg and ':' not in msg and '$' not in msg):
            for session in sessions:
                if loaded_msg[key]["author_id"] in sessions[session]['users_ids']:
                    bot.send_message(sessions[session]['token'], msg)
                    total_sent += 1
        print(f'Сообщение успешно отправлено (всего отправлено {total_sent}).')
        print(f'Перерыв {delay} секунд')
        time.sleep(delay)
    except Exception as e:
        print(f'Что-то пошло не так ERROR: {e.with_traceback}')
        time.sleep(20)