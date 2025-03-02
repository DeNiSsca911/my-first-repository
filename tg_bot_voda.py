import telebot
import datetime
import time
import threading
import random
from telebot import types  # Для создания кнопок

bot = telebot.TeleBot('здесь будет ваш токен')


# Обработчик команды /help
@bot.message_handler(commands=['help'])
def help_message(message):
    # Создаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = types.KeyboardButton('/start')
    btn2 = types.KeyboardButton('/jucy')
    btn3 = types.KeyboardButton('/bodys')
    btn4 = types.KeyboardButton('/fact')
    markup.add(btn1, btn2, btn3, btn4)

    # Отправляем сообщение с клавиатурой
    bot.reply_to(message, "Вот список доступных команд:", reply_markup=markup)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message,
                 'Привет! Я чат бот, который будет напоминать тебе о приеме воды, сока, смузи, напитке Сибири и о физической активности в течение дня!')
    reminder_thread = threading.Thread(target=send_remainders, args=(message.chat.id,))
    reminder_thread.daemon = True  # Поток завершится, если основной поток завершится
    reminder_thread.start()


# Обработчик команды /jucy
@bot.message_handler(commands=["jucy"])
def jucy_message(message):
    bot.reply_to(message,
                 "Свежевыжатый сок богат витаминами, минералами и антиоксидантами, что способствует укреплению иммунной системы, улучшению пищеварения и повышению уровня энергии. Он помогает поддерживать гидратацию и может поддерживать сердечно-сосудистое здоровье благодаря своим свойствам. Однако важно употреблять его в умеренных количествах, так как соки могут содержать много сахара и калорий.")


# Обработчик команды /bodys
@bot.message_handler(commands=["bodys"])
def bodys_message(message):
    bot.reply_to(message,
                 "Регулярная физическая активность имеет огромное значение для здоровья: она укрепляет сердечно-сосудистую систему, помогает контролировать вес, повышает иммунитет, улучшает настроение и сон, а также снижает риск развития хронических заболеваний, таких как диабет и гипертония. Кроме того, спорт поддерживает мышечную силу и здоровье костей, что особенно важно для предотвращения травм и возрастных изменений.")


# Обработчик команды /fact
@bot.message_handler(commands=['fact'])
def fact_message(message):
    facts = [
        "*Вода на Земле может быть старше самой Солнечной системы*: Исследования показывают, что от 30% до 50% воды в наших океанах возможно присутствовала в межзвездном пространстве еще до формирования Солнечной системы около 4,6 миллиарда лет назад.",
        "*Горячая вода замерзает быстрее холодной*: Это явление известно как эффект Мпемба. Под определенными условиями горячая вода может замерзать быстрее, чем холодная, хотя ученые до сих пор полностью не разгадали механизм этого процесса.",
        "*Больше воды в атмосфере, чем во всех реках мира*: Объем водяного пара в атмосфере Земли в любой момент времени превышает объем воды во всех реках мира вместе взятых. Это подчеркивает важную роль атмосферы в гидрологическом цикле, перераспределяя воду по планете."
    ]
    random_fact = random.choice(facts)
    bot.reply_to(message, f"Лови факт о воде:\n{random_fact}", parse_mode="Markdown")


# Функция для отправки напоминаний
def send_remainders(chat_id):
    morning = "07:15"
    first_rem = "08:16"
    second_rem = "12:00"
    therd_rem = "16:00"
    water_rem = "20:00"
    siber_1 = "09:17"
    siber_2 = "13:00"
    siber_3 = "17:00"
    juce1 = "10:18"
    juce2 = "14:00"
    juce3 = "18:00"
    body_1 = "11:19"
    body_2 = "15:00"
    body_3 = "19:00"
    night = "21:20"

    while True:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == morning:
            bot.send_message(chat_id, "Доброе утро! Сегодня тебя ждет замечательный день, просыпайся пожалуйста!")
            time.sleep(61)
        elif now == first_rem or now == second_rem or now == therd_rem or now == water_rem:
            bot.send_message(chat_id, "Напоминание - выпей стакан воды пожалуйста!")
            time.sleep(61)
        elif now == siber_1 or now == siber_2 or now == siber_3:
            bot.send_message(chat_id, "Напоминание - прими очищающий организм напиток Сибири!")
            time.sleep(61)
        elif now == juce1 or now == juce2 or now == juce3:
            bot.send_message(chat_id, "Приготовь для себя и близких свежевыжатый сок или вкусный смузи :)")
            time.sleep(61)
        elif now == body_1 or now == body_2 or now == body_3:
            bot.send_message(chat_id, "Время разогреть свое тело физической активностью -- ДЕРЗАЙ !!!")
            time.sleep(61)
        elif now == night:
            bot.send_message(chat_id, "Сегодня был активный и насыщенный день, приятного отдыха :)")
            time.sleep(61)
        else:
            time.sleep(30)  # Проверяем время каждые 30 секунд


# Запуск бота
bot.polling(none_stop=True)