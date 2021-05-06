import datetime
import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from schedule import sch
from schedule import weekdays_to_words
from bells import bll

vk_session = vk_api.VkApi(token='///')
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

weekday = datetime.datetime.weekday(datetime.datetime.now()) #should correct all of this below
day = sch[weekday]
day_word = weekdays_to_words[weekday]

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
           message = event.text.lower()
           id = event.user_id

           if message == 'расписание':
               to_str = "Завтра " + str(day_word) + '\n' + str(day[0]) + str(day[1]) + str(day[2]) + str(day[3]) + \
                   str(day[4]) + str(day[5]) + str(day[6])
               send(id, to_str)
           elif message == 'полное расписание':
                send(id, '\n' + str(sch[4]))
           elif message == 'замены':
                send(id, '404. Кнопка пока не работает :( Но попробуй другие, наверняка они уже действуют!')
           elif message == 'куратор и зав.отд.':
               send(id, 'Куратор: Писчасова Е. Ф.\nVK: https://vk.com/id21133127\n'
                        'Моб.Тел: +79175026788  (Есть WhatsApp)\n\n'
                        'Зав.отделением: Максимова Т. В.\n'
                        'Моб.Тел: +79104658492 (Есть WhatsApp и Viber)')
           elif message == 'звонки':
               send(id, 'Расписание звонков' + '\n' + str(bll[0]) + str(bll[1]) + str(bll[2]) + str(bll[3]) + \
                    str(bll[4]) + str(bll[5]) + str(bll[6]))
           else:
                send(id, 'бот в стадии разработки!')
