import pymongo
from match import *
from parsing_page import get_soup, get_handicap, get_handicap_by_result, get_id_match
import time
from datetime import datetime
import telebot
from config import BOT_TOKEN, CHAT, TOURNAMENTS, CeF
import math

bot = telebot.TeleBot(BOT_TOKEN)

myclient = pymongo.MongoClient(MONGODB_URI)
dblist = myclient.list_database_names()
db = myclient.test
mydb = myclient["mydatabase"]
mycol = mydb["matches"]

send_content = "Дата: {0}\n" + \
               "Время: {1}\n" + \
               "Турнир: {2}\n" + \
               "Игрок 1: *{3}* (*{4}*)\n " + \
               "Игрок 2: *{5}* (*{6}*)\n" + \
               "Тотал в начале: *{7}*\n" + \
               "Счет: {8}\n" + \
               "Тотал новый: *{9}*\n" + \
               "Соотношения реального тотала и нового: *{10}*"


def get_results(html):
    results = []
    return get_soup(html).find_all('div', {'class': 'cl-left red'})


def get_matches_with_good_results(html):
    mathes_soups = []
    for i in get_results(html):
        if i.text.split()[0] == '0:2' or i.text.split()[0] == '2:0':
            yield ("https://www.marathonbet.com/su/live/" + i.find_parent("div").get("data-event-treeid"))


def get_real_total(s):
    k = s.replace('(', ':').replace(')', ':').replace(',', ':').split(':')
    p = 0
    for i in k[2:-1]:
        p += int(i.split()[0])
    return p


def div_by_result(result):
    id = get_id_match(result)
    soup = get_soup('https://www.marathonbet.com/su/live/' + str(id))
    soup = soup.find("div", {"class": "category-container"})

    matches = {
        'player1': soup.find_all("div", {"class": "live-today-member-name nowrap"})[0].text,
        'player2': soup.find_all("div", {"class": "live-today-member-name nowrap"})[1].text,
        'start_total': get_handicap(soup),
        "player1k": float(soup.find_all("span", {"selection-link normal"})[0].text),
        "player2k": float(soup.find_all("span", {"selection-link normal"})[1].text),
        "tournament": soup.find("h2", {"class": "category-label"}).text
    }
    print(matches)
    return matches


def parse(html, Cf):
    for i in get_results(html):
        if i.text.split()[0] == '2:0' or i.text.split()[0] == '0:2':
            if len(Match.objects(ID=get_id_match(i), posted=False)) > 0 and len(i.text) > 16:
                new_match = Match.objects(ID=get_id_match(i))[0]
                new_match.posted = True
                new_match.save()
                if math.fabs(new_match.player1k - new_match.player2k) <= Cf:
                    finish_total = get_handicap_by_result(i)
                    cof = finish_total - get_real_total(i.text)
                    bot.send_message(CHAT, text=send_content.format(new_match.date,
                                                                    new_match.time,
                                                                    new_match.tournament,
                                                                    new_match.player1,
                                                                    new_match.player1k,
                                                                    new_match.player2,
                                                                    new_match.player2k,
                                                                    new_match.start_total,
                                                                    i.text,
                                                                    finish_total,
                                                                    cof
                                                                    ),
                                     parse_mode='markdown')

        if i.text.split()[0] == '0:0':
            try:
                Match.objects.get(ID=get_id_match(i))

            except:
                x = div_by_result(i)
                for j in TOURNAMENTS:
                    if x['tournament'].find(j) >= 0:
                        Match(time=str(datetime.now()).split()[1].split('.')[0],
                              date=str(datetime.now()).split()[0],
                              ID=get_id_match(i),
                              player1=x['player1'],
                              player2=x['player2'],
                              player1k=x['player1k'],
                              player2k=x['player2k'],
                              start_total=x['start_total'],
                              tournament=x['tournament']).save()


if __name__ == "__main__":
    while True:
        try:
            time.sleep(5)
            parse("https://www.marathonbet.com/su/live/414329", CeF)
        except Exception as e:
            print(e)

    # x = Match(start_total = 9)
    # x.save()

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# dblist=myclient.list_database_names()
# db = myclient.test
# mydb = myclient["mydatabase"]
# mycol = mydb["matches"]
#
# mydict = { "name": "John", "address": "Highway 37" }
# mycol.insert_one(mydict)
# print([x for x in get_matches_with_good_results("https://www.marathonbet.com/su/live/22723")])
