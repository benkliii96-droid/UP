import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import datetime
import json
import random

# Конфигурация
TOKEN = 'vk1.a.TCC1NI4iYiwI1DHqdYupYggz2TfPybDEfZjWjERrv0njKohU2YSRIURzejhDRphRxAmGExWry1ScZSpEe5Ox_wCE_BdWnObLKCUYtchletx-ritkgUoEeTspK-S1JIhgf-_Rls_pdmcXJGBvJcKFXgBlE5t3KbtMuP83Z3ec0QjqSMPyAL7EdjIqyOE0k5TKK4a92AyeaZQmz0-zjEAiSg'
ID = 237336674

# Инициализация API и Long Poll
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, ID)

# Отправка сообщения
def send_message(user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 2 ** 31),
        keyboard=keyboard
    )

# Обычная клавиатура меню
def get_main_menu():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [{"action": {"type": "text", "label": "информация"}, "color": "primary"},
             {"action": {"type": "text", "label": "помощь"}, "color": "positive"}],
            [{"action": {"type": "text", "label": "о боте"}, "color": "secondary"},
             {"action": {"type": "text", "label": "выйти"}, "color": "negative"}]
        ]
    }, ensure_ascii=False)

# Inline-клавиатура с callback-кнопками
def get_inline_keyboard():
    return json.dumps({
        "inline": True,
        "buttons": [
            [{"action": {"type": "callback", "label": "Лайк", "payload": json.dumps({"action": "like"})}, "color": "positive"},
             {"action": {"type": "callback", "label": "Дизлайк", "payload": json.dumps({"action": "dislike"})}, "color": "negative"}],
            [{"action": {"type": "callback", "label": "Далее", "payload": json.dumps({"action": "next"})}, "color": "primary"}]
        ]
    }, ensure_ascii=False)

# Ответ на callback (всплывающее уведомление)
def send_event_answer(event, text):
    vk.messages.sendMessageEventAnswer(
        event_id=event.obj.event_id,
        user_id=event.obj.user_id,
        peer_id=event.obj.peer_id,
        event_data=json.dumps({"type": "show_snackbar", "text": text})
    )

# Главный цикл обработки событий
for event in longpoll.listen():
    # Обработка текстовых сообщений
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_id = event.obj.message['from_id']
        msg = event.obj.message['text'].strip()
        lower_msg = msg.lower()

        if lower_msg == "пока":
            send_message(user_id, "До свидания!")
        elif lower_msg in ("start", "/start"):
            send_message(user_id, "Бот запущен! Напишите 'меню' для продолжения")
        elif lower_msg == "помощь":
            send_message(user_id, "Команды: пока, start, помощь, время, меню, inline, rand")
        elif lower_msg == "время":
            send_message(user_id, f"Текущее время: {datetime.datetime.now().strftime('%H:%M:%S')}")
        elif lower_msg == "меню":
            send_message(user_id, "Главное меню:", keyboard=get_main_menu())
        elif lower_msg == "inline":
            send_message(user_id, "Inline-клавиатура:", keyboard=get_inline_keyboard())
        elif lower_msg in ("rand", "случайное число"):
            send_message(user_id, f"Случайное число: {random.randint(1, 100)}")
        elif msg == "информация":
            send_message(user_id, "Я бот инвалид.")
        elif msg == "о боте":
            send_message(user_id, "Бот придурок.")
        elif msg == "выйти":
            empty_kb = json.dumps({"one_time": False, "buttons": []})
            send_message(user_id, "Клавиатура скрыта. Напишите 'меню' для возврата.", keyboard=empty_kb)
        else:
            send_message(user_id, "Привет!")

    # Обработка callback-событий от inline-кнопок
    elif event.type == VkBotEventType.MESSAGE_EVENT:
        payload = event.obj.payload
        action = payload.get('action')
        if action == 'like':
            send_event_answer(event, "Вы поставили лайк!")
        elif action == 'dislike':
            send_event_answer(event, "Вы поставили дизлайк!")
        elif action == 'next':
            send_event_answer(event, "Переход к следующему...")
        else:
            send_event_answer(event, "Неизвестное действие")