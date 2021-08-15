import telebot
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
from telebot import types
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def send_welcom(massage):
    bot.send_message(massage.chat.id,"Howdy, I can send you the weather in Bilopillya city, show realy beautiful instagram and I'll help you to find job on junior python developer position in Poland or Ukraine. Good luck and have fan \nFor check commands type /help")

@bot.message_handler(commands=['help'])
def send_commands(massage):
    bot.send_message(massage.chat.id,'Allows command:\n /weather (To see what is the weather in Bilopillya)\n /instagram (To see Nelya Holik instagram)\n /pracuj (To see job offers in Poland website "Pracuj.pl")\n /rabota (To see job offers in Ukraine website "rabota.ua")')

@bot.message_handler(commands=['weather'])
def send_weather(massage):
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
            print(day,'\n',date,month,'\n', t_min, t_max)
            print(descr)
        bot.send_message(massage.chat.id,'The weather in ' + city + ' city:\n' +
            day + '\n' + date +' '+ month +'\n'+ t_min +' '+ t_max +'\n'+ descr)
    weather_at(url="https://sinoptik.ua/погода-белополье", city='Bilopillya')
    weather_at(url="https://sinoptik.ua/погода-киев", city='Kiev')
    weather_at(url="https://sinoptik.ua/погода-сумы", city='Sumy')
    weather_at(url="https://sinoptik.ua/погода-харьков", city='Kharkiv')
    weather_at(url="https://sinoptik.ua/погода-львов", city='Lviv')

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
