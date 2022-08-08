import requests
import json
from pprint import pprint

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

TOKEN = '토큰'

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello! I am bot!")

def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.message.chat_id, text=text_caps)

def weather(update, context):
    res = requests.get('https://api.openweathermap.org/data/2.5/weather?q=daegu,kr&appid=토큰')
    data = json.loads(res.content)

    weather = data['weather'][0]['main']
    temp = data['main']['temp'] - 273.15
    humidity = data['main']['humidity']
    text = f'현재 날씨는 {weather}이며, 기온은 {temp}℃, 습도는 {humidity}% 입니다.'
    
    context.bot.send_message(chat_id=update.message.chat_id, text=text)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & ~Filters.command, echo)
caps_handler = CommandHandler('caps', caps)
weather_handler = CommandHandler('weather', weather)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(weather_handler)

updater.start_polling()