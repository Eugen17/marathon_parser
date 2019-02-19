import requests
from bs4 import BeautifulSoup
import pymongo



def get_soup(html):
    res = requests.get(html)
    soup = BeautifulSoup(res.text, features="html.parser")
    return soup



def get_id_match(result):
    return result.find_parent("div").get("data-event-treeid")


def get_handicaps_soups(type_of_bet, html):
    price = []
    price = get_soup(html).find_all('div', {'class': 'name-field'})
    for i in price:
        if i.text.strip() == type_of_bet:
            price = i
            break
    price = price.find_parent('table').find_next('table').find_all('div', {'class': 'coeff-handicap'})
    handicaps = []
    for i in price:
        handicaps.append(float(i.text.strip()[1:-1]))
    return handicaps

def get_handicap(soup):
    price = soup.find_all('div', {'class': 'name-field'})
    price1 = []
    for i in price:
        if i.text.strip() == "Тотал матча по очкам":
            price1 = i.find_parent('table').find_next('table').find_all('div', {'class': 'coeff-handicap'})
            break
    handicaps = []
    for i in price1:
        handicaps.append(float(i.text.strip()[1:-1]))
    return max(handicaps)

def get_handicap_by_result(soup):
    id = get_id_match(soup)
    soup = get_soup('https://www.marathonbet.com/su/live/' + str(id))
    soup = soup.find("div", {"class": "category-container"})
    price = soup.find_all('div', {'class': 'name-field'})
    price1 = []
    for i in price:
        if i.text.strip() == "Тотал матча по очкам":
            price1 = i.find_parent('table').find_next('table').find_all('div', {'class': 'coeff-handicap'})
            break
    handicaps = []
    for i in price1:
        handicaps.append(float(i.text.strip()[1:-1]))
    return max(handicaps)



def get_string_result():
    pass


def get_match_link():
    pass


def is_2_0_result():
    pass


def result_good():
    pass


def is_match_in_db():
    pass


def get_first_cf():
    pass


if __name__ == "__main__":
    print(get_handicap(get_soup(
                        "https://www.marathonbet.com/su/live/414329")))
