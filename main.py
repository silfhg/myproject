import telebot
import datetime
import threading

bot = telebot.TeleBot('7157111428:AAESL5i36HCrMykQdHUS9zutT6RixEfmzE8')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'приветик! я бот-напоминалка. введите /reminder, чтобы вы смогли установить '
                                      'напоминание')


@bot.message_handler(commands=['reminder'])
def reminder_message(message):
    bot.send_message(message.chat.id, 'введите название напоминания')
    bot.register_next_step_handler(message, set_reminder_name)


def set_reminder_name(message):
    user_data = {}
    user_data[message.chat.id] = {'reminder_name': message.text}
    bot.send_message(message.chat.id, 'введите дату и время, '
                                      'когда вы хотите получить напоминание в формате ГГГГ-ММ-ДД чч:мм:сс.')
    bot.register_next_step_handler(message, reminder_set, user_data)


def reminder_set(message, user_data):
    try:
        reminder_time = datetime.datetime.strptime(message.text, '%Y-%m-%d %H:%M:%S')
        now = datetime.datetime.now()
        delta = reminder_time - now
        if delta.total_seconds() <= 0:
            bot.send_message(message.chat.id, 'вы ввели уже прошедшую дату, попробуйте еще раз')
        else:
            reminder_name = user_data[message.chat.id]['reminder_name']
            bot.send_message(message.chat.id, 'напоминание "{}" установлено на {}'.format(reminder_name,
                                                                                           reminder_time))
            reminder_timer = threading.Timer(delta.total_seconds(), send_reminder,
                                             [message.chat.id, reminder_name])
            reminder_timer.start()
    except ValueError:
        bot.send_message(message.chat.id, 'вы ввели неверный формат даты и времени, попробуйте еще раз')


def send_reminder(chat_id, reminder_name):
    bot.send_message(chat_id, 'не забудьте, что вы должны "{}"!'.format(reminder_name))


@bot.message_handler(func=lambda message: True)
def handle_all_message(message):
    bot.send_message(message.chat.id, 'я не понимаю, что вы имеете ввиду. чтобы создать напоминание вы должны'
                                      ' ввести /reminder')


if __name__ == '__main__':
    bot.polling(none_stop=True)
