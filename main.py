import datetime
import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from schedule import sch
from schedule import weekdays_to_words

vk_session = vk_api.VkApi(token='token')
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
        [get_butt('Звонки', 'positive'), get_butt('Список преподавателей', 'positive')]
    ]
}

keyboard = json.dumps(keyboard, ensure_ascii = False).encode('utf-8')
keyboard = str (keyboard.decode('utf-8'))

def send(id, text):
    session_api.messages.send(user_id = id, message = text, random_id = 0, keyboard = keyboard)

weekday = datetime.datetime.weekday(datetime.datetime.now()) + 1 #should correct all of this below
day = sch[weekday + 1]
day_word = weekdays_to_words[weekday]

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
           message = event.text.lower()
           id = event.user_id

           if message == 'расписание':
               to_str = "Завтра " + str(day_word) + str(day)
               # to_str = str(weekday)
               send(id, to_str)
           elif message == 'полное расписание':
                send(id, 'asdasd')
           elif message == 'замены':
                send(id, '404. Кнопка пока не работает :( Но попробуй другие, наверняка они уже действуют!')
           elif message == 'куратор и зав.отд.':
               send(id, 'Куратор: Писчасова Е. Ф.\nVK: https://vk.com/id21133127\n'
                        'Моб.Тел: +79175026788  (Есть WhatsApp)\n\n'
                        'Зав.отделением: Максимова Т. В.\n'
                        'Моб.Тел: +79104658492 (Есть WhatsApp и Viber)')
           else:
                send(id, 'бот в стадии разработки!')
