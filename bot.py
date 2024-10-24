import os

import telebot
import requests
from bs4 import BeautifulSoup as bs
from telebot import types

TOKEN = os.environ["TOKEN"]

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcom(massage):
    bot.send_message(massage.chat.id,"Howdy, I can send you the weather in some Ukrainian cities, show realy beautiful instagram and I'll help you to find job on junior python developer position in Poland or Ukraine. Good luck and have fan \nFor check commands type /help")

@bot.message_handler(commands=['help'])
def send_commands(massage):
    bot.send_message(massage.chat.id,'Allows command:\n /weather (To see what is the weather in some Ukrainian cities)\n /instagram (To see Nelya Holik instagram)\n /pracuj (To see job offers in Poland website "Pracuj.pl")\n /rabota (To see job offers in Ukraine website "rabota.ua")')

@bot.message_handler(commands=['weather'])
def get_city(massage):

    markup_inline = types.InlineKeyboardMarkup()
    item_bilopillya = types.InlineKeyboardButton(text='Bilopillya', callback_data='Bilopillya')
    item_kiev = types.InlineKeyboardButton(text='Kiev', callback_data='Kiev')
    item_sumy = types.InlineKeyboardButton(text='Sumy', callback_data='Sumy')
    item_kharkiv = types.InlineKeyboardButton(text='Kharkiv', callback_data='Kharkiv')
    item_lviv = types.InlineKeyboardButton(text='Lviv', callback_data='Lviv')
    item_khmelnitsky = types.InlineKeyboardButton(text='Khmelnitsky', callback_data='Khmelnitsky')
    item_drohobych = types.InlineKeyboardButton(text='Drohobych', callback_data='Drohobych')

    markup_inline.add(item_bilopillya, item_sumy, item_kiev, item_khmelnitsky, item_lviv, item_drohobych, item_kharkiv)
    bot.send_message(massage.chat.id, 'Choose the city in which you want to see the weather for today', reply_markup=markup_inline)

@bot.callback_query_handler(func = lambda call: True)
def weather_answer(call):
    def weather_at(url, city):
        r = requests.get(url)
        html = bs(r.content,'html.parser')

        for elem in html.select('#content'):
            day = elem.select('.tabs .day-link')[0].text
            date = elem.select('.tabs .date')[0].text
            month = elem.select('.tabs .month')[0].text
            t_min = elem.select('.temperature .min')[0].text
            t_max = elem.select('.temperature .max')[0].text
            descr = elem.select('.wDescription .description')[0].text
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='The weather in ' + city + ' city:\n' +
            day + '\n' + date +' '+ month +'\n'+ t_min +' '+ t_max +'\n'+ descr)

    if call.data == 'Bilopillya':
        weather_at(url="https://sinoptik.ua/погода-белополье", city='Bilopillya')
    elif call.data == 'Kiev':
        weather_at(url="https://sinoptik.ua/погода-киев", city='Kiev')
    elif call.data == 'Sumy':
        weather_at(url="https://sinoptik.ua/погода-сумы", city='Sumy')
    elif call.data == 'Kharkiv':
        weather_at(url="https://sinoptik.ua/погода-харьков", city='Kharkiv')
    elif call.data == 'Lviv':
        weather_at(url="https://sinoptik.ua/погода-львов", city='Lviv')
    elif call.data == 'Khmelnitsky':
        weather_at(url="https://sinoptik.ua/погода-хмельницкий", city='Khmelnitsky')
    else:
        weather_at(url="https://sinoptik.ua/погода-дрогобыч", city='Drohobych')

@bot.message_handler(commands=['instagram'])
def send_link(massage):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Check the best Instagram",url="https://www.instagram.com/neliaholik/"))
    bot.send_message(massage.chat.id,"Ok here the best instagram in the world",parse_mode='html',reply_markup=markup)

@bot.message_handler(commands=['pracuj'])
def send_job_pl(massage):
    soup = requests.get("https://www.pracuj.pl/praca/programista%20python;kw?rd=30&et=17")
    html = bs(soup.content ,'html.parser')
    x = 1
    for elem in html.select(".results__list-container-item"):
        if elem.select(".offer-details__title"):
            title = elem.select(".offer-details__title")
            bot.send_message(massage.chat.id,'Position ' +
            "{} : {}".format(x, title[0].text))
            x += 1
            link = elem.a
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(title[0].text, url=link.get('href')))
            bot.send_message(massage.chat.id,"Link bellow",parse_mode='html',reply_markup=markup)

@bot.message_handler(commands=['rabota'])
def send_job_ua(massage):
    soup = requests.get("https://rabota.ua/zapros/junior-python-developer/%D1%83%D0%BA%D1%80%D0%B0%D0%B8%D0%BD%D0%B0")
    html = bs(soup.content ,'html.parser')
    num = 1
    res_table = html.table
    for elem in res_table:
        if num == 11:
            break
        title = elem.select(".common-info .card-title")
        bot.send_message(massage.chat.id,'Position ' +
        "{} : {}".format(num, title[0].text))
        num += 1
        link = elem.a
        first_part_of_link = 'https://rabota.ua'
        full_link = first_part_of_link + link.get('href')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(title[0].text, url=full_link))
        bot.send_message(massage.chat.id,"Link bellow",parse_mode='html',reply_markup=markup)

bot.polling()
