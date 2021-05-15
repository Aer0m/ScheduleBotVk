import datetime
import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import os
from parse import group_id, album_id
from group_token import tok
from schedule import sch
from schedule import weekdays_to_words
from schedule import wd_words
from bells import bll
from teacher_list import teachers

vk_session = vk_api.VkApi(token = tok)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def get_butt(text, color):
    return {
            "action": {
                "type": "text",
                "payload": "{\"button\": \"" + "1" + "\"}",
                "label": f"{text}"
            },
            "color": f"{color}"
    }

keyboard = {
    "one_time": False,
    "buttons": [
        [get_butt('Расписание', 'positive'), get_butt('Полное расписание', 'positive')],
        [get_butt('Замены', 'positive'), get_butt('Куратор и зав.отд.', 'positive')],
        [get_butt('Звонки', 'positive'), get_butt('Список преподавателей', 'positive')],
        [get_butt('До конца семестра осталось', 'positive'), get_butt('Сообщить об ошибке', 'negative')]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
keyboard = str (keyboard.decode('utf-8'))

def send(id, text):
    session_api.messages.send(user_id = id, message = text, random_id = 0, keyboard = keyboard)

def send_pic(id, url):
    session_api.messages.send(user_id = id, attachment = url, random_id = 0, keyboard = keyboard)

def photo(user_id):
    a = vk_session.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open('C:/Users/Sekira-Andy/Downloads', 'rb')}).json()
    c = vk_session.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk_session.method("messages.send", {"peer_id": user_id, "message": "Замены:", "attachment": f'photo{c["owner_id"]}_{c["id"]}'})

def write_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def get_upload_server():
    r = requests.get('https://api.vk.com/method/photos.getUploadServer', params={
        'acces_token': tok,
        'album_id': album_id,
        'group_id': group_id
    }).json()

weekday = datetime.datetime.weekday(datetime.datetime.now())
teachers = str(teachers)
teachers = teachers.split(",")
teachers = '\n\n'.join(teachers)
teachers = teachers.strip('[')
teachers = teachers.strip(']')
teachers = teachers.strip()

if(weekday < 5):
    day = sch[weekday]
    day_word = weekdays_to_words[weekday]
else:
    day = sch[0]
    day_word = weekdays_to_words[0]

def main():
   # upload_url = get_upload_server()

    #file = {'file1': open()}
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
               message = event.text.lower()
               id = event.user_id

               if message == 'расписание' and day == 3:
                   to_str = "Расписание  на " + str(day_word) + ':\n\n' + str(day[0]) + str(day[1]) + str(day[2]) + str(day[3]) + \
                       str(day[4]) + str(day[5]) + str(day[6]) + str(day[7]) + str(day[8])
                   send(id, to_str)
               elif message == 'расписание':
                   to_str = "Расписание  на " + str(day_word) + ':\n______________________________\n' + str(day[0]) + str(day[1]) + \
                   str(day[2]) + str(day[3]) + str(day[4]) + str(day[5]) + str(day[6])
                   send(id, to_str)
               elif message == 'полное расписание':
                   full_sch = str(wd_words[0]) + '\n' + str(sch[0][0]) + str(sch[0][1]) + str(sch[0][2]) + str(sch[0][3]) \
                   + str(sch[0][4]) + str(sch[0][5]) + str(sch[0][6]) + '\n\n' \
                   + str(wd_words[1]) + '\n' + str(sch[1][0]) + str(sch[1][1]) + str(sch[1][2]) + str(sch[1][3]) + str(sch[1][4]) \
                   + str(sch[1][5]) + str(sch[1][6]) + '\n\n' \
                   + str(wd_words[2]) + '\n' + str(sch[2][0]) + str(sch[2][1]) + str(sch[2][2]) + str(sch[2][3]) + str(sch[2][4]) \
                   + str(sch[2][5]) + str(sch[2][6]) + '\n\n' \
                   + str(wd_words[3]) + '\n' + str(sch[3][0]) + str(sch[3][1]) + str(sch[3][2]) + str( sch[3][3]) + str(sch[3][4]) \
                   + str(sch[3][5]) + str(sch[3][6]) + str(sch[3][7]) + str(sch[3][8]) + '\n\n' \
                   + str(wd_words[4]) + '\n' + str(sch[4][0]) + str(sch[4][1]) + str(sch[4][2]) + str(sch[4][3]) + str(sch[4][4]) \
                   + str(sch[4][5]) + str(sch[4][6])
                   send(id, full_sch)
               elif message == 'замены':
                    send_pic(id, 'photo-192707383_457239021')
                    send_pic(id, 'photo-192707383_457239022')
                    send(id, 'https://collegetsaritsyno.mskobr.ru/attach_files/upload_users_files/609e86f20baca.pdf')
               elif message == 'куратор и зав.отд.':
                   send(id, 'Куратор: Писчасова Е. Ф.\nVK: https://vk.com/id21133127\n'
                            'Моб.Тел: +79175026788  (Есть WhatsApp)\n\n'
                            'Зав.отделением: Максимова Т. В.\n'
                            'Моб.Тел: +79104658492 (Есть WhatsApp и Viber)')
               elif message == 'звонки':
                   send(id, 'Расписание звонков' + '\n' + str(bll[0]) + str(bll[1]) + str(bll[2]) + str(bll[3]) + \
                        str(bll[4]) + str(bll[5]) + str(bll[6]))
               elif message == 'сообщить об ошибке':
                   send(id, 'Тут будет ссылка на беседу...')
               elif message == 'список преподавателей':
                   send(id, teachers)
               elif message == 'до конца семестра осталось':
                   send(id, 'Кнопка пока не работает, но скоро заработает...')
               elif message == 'debug':         #ф-ция разраба для дебага функций, переменных, массивов и т.д.
                   send(id, wd_words[0])
               elif id == 67859068 and message == 'bot_shutdown':
                   send(id, '->bot_powered_off')
                   raise SystemExit(1)
               elif id != 67859068 and message == 'bot_shutdown':
                   send(id, 'У вас нет прав на эту команду.')
               elif message == 'bot_dev_left': #ф-ция разраба узнать о дальнейших разработках
                   send(id, 'Осталось разработать или доработать ещё 3 кнопки:\n' + 'Полное расписание\n' \
                        + 'До конца семестра осталось\n' + 'Замены')
               elif id == 67859068 and message == 'bot_restart':
                   send (id, '->bot_restarted')
                   main()
               elif id != 67859068 and message == 'bot_restart':
                   send(id, 'У вас нет прав на эту команду.')
               elif message == 'начать':
                   send(id, 'Рад приветстовать! Начинаем работу.')
               else:
                    send(id, 'Команда была введена неверно! Если у вас есть идеи по введению новых функций и поправок, '
                             'или вы считаете, что бота требуется перезапустить, обратитесь к разработчку.')

while True:
    main()

    try:
        os.system("python3 main.py")
    except:
        pass