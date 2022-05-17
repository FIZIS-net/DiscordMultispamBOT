from urllib import request
from threading import *
from spamBot import spamBot
import requests as r
import os, random
from random import randint
from time import time, sleep
import json
import base64

id_copied_chat = input(f'Enter the chat id from where to copy messages: ')
id_insert_chat = input(f'Enter the chat id where to copy messages: ')
messages_count = int(input(f'Enter a multiple of 100 messages: '))
delay_start = int(input(f'Enter the minimum delay on the server: '))
delay_end = int(input(f'Enter the maximum delay: '))
typing_delay = int(input(f'Enter the print delay: '))

bot = spamBot(id_copied_chat, id_insert_chat)
tokens_list = open('tokens.txt', 'r', encoding='utf-8').read().splitlines()

firs_session = bot.create_session(tokens_list[1])
loaded_msg = bot.get_messages(firs_session)

all_messages = {}
all_messages.update(loaded_msg)
for i in range(0, (messages_count//100)):
    loaded_msg = bot.get_messages_before(firs_session, bot.get_last_messages_id(all_messages))
    all_messages.update(loaded_msg)

users_ids = []
for message in all_messages:
    if all_messages[message]['author_id'] not in  users_ids:
        users_ids.append(all_messages[message]['author_id'])

def cooldownMessage(sec):
    sleep(sec)

random.shuffle(users_ids)

sessions = {}
sessions_count = 0
# проходимся по всем токенам и создаём сессии
for token in tokens_list:
    sessions[sessions_count] = {"token": bot.create_session(token), "users_ids": [], "thread": Thread(target = cooldownMessage, args=(randint(delay_start, delay_end),))}
    # file = random.choice(os.listdir("avatars"))
    # with open('avatars/'+ file, "rb") as img_file:
    #     avatar = base64.b64encode(img_file.read()).decode('utf-8')
    #     bot.set_avatar(avatar,sessions[sessions_count]["token"])
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


# проходимся циклом по всем сообщениям
for key in loaded_msg:
    try:
        msg = loaded_msg[key]
        delay = random.randint(delay_start, delay_end)
        if('https://' not in msg["message_content"] and ':' not in msg["message_content"] and '$' not in msg["message_content"]):
            # проходимя циклом по всем сессиям
            for session in sessions:
                # проверяем совпадвет ли хоть один id присвоенный боту с id юзера
                if loaded_msg[key]["author_id"] in sessions[session]['users_ids']:
                    if not sessions[session]["thread"].is_alive():
                        try:
                            sessions[session]["thread"].start()
                        except:
                            sessions[session]["thread"] = Thread(target = cooldownMessage, args=(randint(delay_start, delay_end),))
                            sessions[session]["thread"].start()
                        # бот отправляет набор текста
                        bot.send_typing(sessions[session]['token'])
                        # бот ждёт окончание задержки на печать текста
                        sleep(typing_delay)
                        # отправляем сообщение
                        try:
                            req = bot.send_message(sessions[session]['token'], msg, sent_msg)
                            # записываем id отправленного сообщения в массив
                            sent_msg[key] = {"msg_id": req["id"]}
                            total_sent += 1
                            print(req['author']['username'] + " : " + req['content'] + "\n (всего отправлено " + str(total_sent) + ")")
                        except Exception as e:
                            print('error')
                    else:
                        sessions[session]["thread"].join()
                        # бот отправляет набор текста
                        bot.send_typing(sessions[session]['token'])
                        # бот ждёт окончание задержки на печать текста
                        sleep(typing_delay)
                        # отправляем сообщение
                        try:
                            req = bot.send_message(sessions[session]['token'], msg, sent_msg)
                            # записываем id отправленного сообщения в массив
                            sent_msg[key] = {"msg_id": req["id"]}
                            total_sent += 1
                            print(req['author']['username'] + " : " + req['content'] + "\n (всего отправлено " + str(total_sent) + ")")
                        except Exception as e:
                            print('error')
        

    except Exception as e:
        print(f'Что-то пошло не так ERROR: {e.with_traceback}')
        sleep(20)
