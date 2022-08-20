import Scheduler, telebot


TOKEN = ''  # paste your telegram bot token
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('📝 Today schedule')
    btn2 = telebot.types.KeyboardButton('📅 General schedule')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text='Hi! I\'ll give you dayly schedule!'.format(message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == '📝 Today schedule':
        bot.send_message(message.chat.id, text=Scheduler.today_sched())
    elif message.text == '📅 General schedule':
        bot.send_message(message.chat.id, text=Scheduler.full_sched())

bot.polling(none_stop=True)
