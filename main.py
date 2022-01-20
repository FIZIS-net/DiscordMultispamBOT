from turtle import delay
from spamBot import spamBot
import random
import time
first_discord_token = input(f'Введите токен первого аккаунта: ')
second_discord_token = input(f'Введите токен первого аккаунта: ')
id_copied_chat = input(f'Введите id чата откуда копировать сообщения: ')
id_insert_chat = input(f'Введите id чата куда копировать сообщения: ')
messages_count = int(input(f'Введите число сообщений кратное 100: '))
dlay_start = int(input(f'Введите от скольки секунд делать задержку: '))
delay_end = int(input(f'Введите до скольки секунд делать задержку: '))

bot = spamBot(id_copied_chat, id_insert_chat)

firs_session = bot.create_session(first_discord_token)
second_session = bot.create_session(second_discord_token)

loaded_msg = bot.get_messages(firs_session)
all_messages = {}
all_messages.update(loaded_msg)

for i in range(0, (messages_count//100)):
    loaded_msg = bot.get_messages_before(firs_session, bot.get_last_messages_id(all_messages))
    all_messages.update(loaded_msg)
    print(all_messages)


loaded_msg = bot.reverseDict(all_messages)
total_sent = 0
for key in loaded_msg:
    try:
        msg= loaded_msg[key]["message_content"]
        print(f'Sending message {msg}')
        _data = {'content':msg, 'tts':False}
        delay = random.randint(dlay_start, delay_end)
        if('https://' not in msg and ':' not in msg and '$' not in msg):
            if bool(random.getrandbits(1)):
                bot.send_message(firs_session, msg)
                total_sent += 1
            else:
                bot.send_message(second_session, msg)
                total_sent += 1

        print(f'Сообщение успешно отправлено (всего отправлено {total_sent}).')
        print(f'Перерыв {delay} секунд')
        time.sleep(delay)
    except Exception as e:
        print(f'Что-то пошло не так ERROR: {e}')
        time.sleep(20)