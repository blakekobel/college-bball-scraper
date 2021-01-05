import datetime as dt
from bs4 import BeautifulSoup
import urllib
import sys
import requests
import db_helper
import pandas as pd


def scrape_games():
    today = dt.date.today()
    today_db = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db = db_helper.Db_Helper()

    teams = db.get_teams()
    tf = pd.DataFrame(teams, columns=['teamID','kenpom_name','sr_name','bpi_name','sr_games_name','odds_api_name','extra_name3'])
    print(tf)
    
    game_list = []

    today_url = "https://www.sports-reference.com/cbb/boxscores/index.cgi?month="+str(today.month)+"&day="+str(today.day)+"&year="+str(today.year)
    sref_games = requests.get(today_url)
    soup_sref = BeautifulSoup(sref_games.content, 'lxml')
    sref_table = soup_sref.findAll("div",{"class":"game_summary nohover"})
    for x in sref_table:
        if x.find("tbody").findAll("tr")[0].find("a").has_attr('href') and x.find("tbody").findAll("tr")[1].find("a").has_attr('href'):
            teamname1 =x.find("tbody").findAll("tr")[0].find("a").text
            teamname2 =x.find("tbody").findAll("tr")[1].find("a").text
            # print(teamname1,teamname2)
            if "-" in teamname1 or "(" in teamname1 or ")" in teamname1 or "." in teamname1:
                teamname1 = teamname1.replace("-", " ")
                teamname1 = teamname1.replace("(", "")
                teamname1 = teamname1.replace(")", "")
                teamname1 = teamname1.replace(".", "")
            # print(tf[tf['sr_games_name'] == teamname1]['teamID'].values[0])
            away_id = tf[tf['sr_games_name'] == teamname1]['teamID'].values[0]
            if "-" in teamname2 or "(" in teamname2 or ")" in teamname2 or "." in teamname2:
                teamname2 = teamname2.replace("-", " ")
                teamname2 = teamname2.replace("(", "")
                teamname2 = teamname2.replace(")", "")
                teamname2 = teamname2.replace(".", "")
            # print(tf[tf['sr_games_name'] == teamname2]['teamID'].values[0])
            home_id = tf[tf['sr_games_name'] == teamname2]['teamID'].values[0]
            
            game_list.append((today_db,home_id,away_id))
        else:
            pass
    print(game_list)
    return game_list

scrape_games()