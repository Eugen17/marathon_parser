import telebot

from config import BOT_TOKEN, CHAT

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    pass

bot.send_message(1001353156070, "123")
bot.polling(none_stop= True)
