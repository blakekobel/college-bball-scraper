import datetime as dt
from bs4 import BeautifulSoup
import urllib
import sys
import requests


def scrape_games():
    today = dt.date.today()
    game_list = []

    today_url = "https://www.sports-reference.com/cbb/boxscores/index.cgi?month=" + \
        str(today.month)+"&day="+str(today.day)+"&year="+str(today.year)
    print(today_url)
    sref_games = requests.get(today_url)
    soup_sref = BeautifulSoup(sref_games.content, 'lxml')
    sref_table = soup_sref.findAll("div", {"class": "game_summary nohover"})
    for x in sref_table:
        # .has_attr('href'):
        if x.find("tbody").findAll("tr")[0].find("a") and x.find("tbody").findAll("tr")[1].find("a"):
            teamname1 = x.find("tbody").findAll("tr")[0].find("a").text
            teamname2 = x.find("tbody").findAll("tr")[1].find("a").text
            if "-" in teamname1 or "(" in teamname1 or ")" in teamname1 or "." in teamname1:
                teamname1 = teamname1.replace("-", " ")
                teamname1 = teamname1.replace("(", "")
                teamname1 = teamname1.replace(")", "")
                teamname1 = teamname1.replace(".", "")
            if "-" in teamname2 or "(" in teamname2 or ")" in teamname2 or "." in teamname2:
                teamname2 = teamname2.replace("-", " ")
                teamname2 = teamname2.replace("(", "")
                teamname2 = teamname2.replace(")", "")
                teamname2 = teamname2.replace(".", "")
            game_list.append((teamname1, teamname2))
        else:
            pass

    for game in game_list:
        print(game)


scrape_games()
