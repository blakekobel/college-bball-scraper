# This file scrapes and gives scores
from bs4 import BeautifulSoup
import urllib
import sys
import requests
import operator
import datetime
import pandas as pd


def add_ken_pom(KP, date, tf):

    kp_array = []
    kenpom = requests.get(KP)
    soup_kenpom = BeautifulSoup(kenpom.content, 'lxml')
    kenpom_table = soup_kenpom.find("table", {"id": "ratings-table"})
    kenpom_table.findAll("tr")[2].findAll("td")[4]

    for x in kenpom_table.findAll("tr"):
        if x.find("a") == None or x.find("td") == None:
            pass
        else:
            team = x.find("a").text
            #rank = int(x.find("td").text)
            val = x.findAll("td")[4].text
            if team in tf['kenpom_name'].unique():
                teamID = tf[tf['kenpom_name'] == team]['id'].values[0]
                kp_array.append((teamID, "KenPom", val, date))
            else:
                raise ValueError(str(team) + ' doesnt match the kenpom names')

    return kp_array

# # This section adds BPI to the teams_dict


def add_BPI(BP, date, tf):
    bpi_array = []
    for link in BP:
        r = requests.get(link)
        soup2 = BeautifulSoup(r.content, 'lxml')
        table = soup2.find("table", {"class": "bpi__table"})
        if table is None:
            continue
        for x in table.find("tbody").findAll("tr"):
            if x.find("a") == None or x.find("td") == None:
                pass
            else:
                team = x.find("span", {"class": "team-names"}).text
                rank = x.findAll("td")[0].text
                val = x.findAll("td")[6].text
                if team in tf['bpi_name'].unique():
                    teamID = tf[tf['bpi_name'] == team]['id'].values[0]
                    bpi_array.append((teamID, "BPI", val, date))
                else:
                    raise ValueError(str(team) + ' doesnt match the bpi names')
    return bpi_array

# #  This Section brings in SRS to teams


def add_sports_ref(SRS, date, tf):
    srs_array = []
    srs = requests.get(SRS)
    soup_srs = BeautifulSoup(srs.content, 'lxml')
    srs_table = soup_srs.find("table", {"id": "ratings"})

    for x in srs_table.find("tbody").findAll("tr"):
        if x.find("a") == None:
            pass
        else:
            team = x.find("a").text
            srs_val = x.findAll("td")[14].text
            o_eff = x.findAll("td")[15].text
            d_eff = x.findAll("td")[16].text
            ppg = x.findAll("td")[6].text
            papg = x.findAll("td")[7].text

            if team in tf['sr_name'].unique():
                teamID = tf[tf['sr_name'] == team]['id'].values[0]
                srs_array.append((teamID, "SRS", srs_val, date))
                srs_array.append((teamID, "O_Efficiency", o_eff, date))
                srs_array.append((teamID, "D_Efficiency", d_eff, date))
                srs_array.append((teamID, "PPG", ppg, date))
                srs_array.append((teamID, "PAPG", papg, date))
            else:
                raise ValueError(
                    str(team) + ' doesnt match the Sports Ref names')

    return srs_array


def add_advanced(date, tf):
    srs_adv_array = []
    SR_ratings_team = "https://www.sports-reference.com/cbb/seasons/2021-advanced-school-stats.html"
    SR_ratings_opp = "https://www.sports-reference.com/cbb/seasons/2021-advanced-opponent-stats.html"

    team_ratings = requests.get(SR_ratings_team)
    team_soup_ratings = BeautifulSoup(team_ratings.content, 'lxml')
    team_ratings_table = team_soup_ratings.find(
        "table", {"id": "adv_school_stats"})
    teams = team_ratings_table.find("tbody").findAll("tr")

    opp_ratings = requests.get(SR_ratings_opp)
    opp_soup_ratings = BeautifulSoup(opp_ratings.content, 'lxml')
    opp_ratings_table = opp_soup_ratings.find("table", {"id": "adv_opp_stats"})
    opps = opp_ratings_table.find("tbody").findAll("tr")

    for x in teams:
        if x.find("a") == None or x.findAll("td")[16] == None:
            pass
        else:
            team = x.find('a').text
            pace = x.findAll('td')[16].text
            Three_Par = x.findAll('td')[19].text
            TS = x.findAll('td')[20].text
            Tov = x.findAll('td')[26].text

            if team in tf['sr_name'].unique():
                teamID = tf[tf['sr_name'] == team]['id'].values[0]
                srs_adv_array.append((teamID, "Pace", pace, date))
                srs_adv_array.append(
                    (teamID, "Three_Point_Attempt_Rate", Three_Par, date))
                srs_adv_array.append((teamID, "True_Shooting", TS, date))
                srs_adv_array.append((teamID, "Turnover_Perc", Tov, date))
            else:
                raise ValueError(
                    str(team) + ' doesnt match the Sports Ref names')
    for x in opps:
        if x.find("a") == None or x.findAll("td")[16] == None:
            pass
        else:
            team = x.find('a').text
            pace = x.findAll('td')[16].text
            Three_Par = x.findAll('td')[19].text
            TS = x.findAll('td')[20].text
            Tov = x.findAll('td')[26].text

            if team in tf['sr_name'].unique():
                teamID = tf[tf['sr_name'] == team]['id'].values[0]
                srs_adv_array.append(
                    (teamID, "Opp_Three_Point_Attempt_Rate", Three_Par, date))
                srs_adv_array.append((teamID, "Opp_True_Shooting", TS, date))
                srs_adv_array.append((teamID, "Opp_Turnover_Perc", Tov, date))
            else:
                raise ValueError(
                    str(team) + ' doesnt match the Sports Ref names')

    return srs_adv_array


def get_teams():
    dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tf = pd.read_csv("teams_table.csv")
    KP = 'https://kenpom.com/'
    BP = []
    for x in range(1, 16):
        BP.append(
            'http://www.espn.com/mens-college-basketball/bpi/_/view/bpi/page/' + str(x))
    SRS = "https://www.sports-reference.com/cbb/seasons/2021-ratings.html"

    kp_arr = add_ken_pom(KP, dt, tf)
    bpi_arr = add_BPI(BP, dt, tf)
    srs_arr = add_sports_ref(SRS, dt, tf)
    srs_adv_arr = add_advanced(dt, tf)

    final = kp_arr + bpi_arr + srs_arr + srs_adv_arr
    df = pd.DataFrame(final, columns=['teamID', 'metric', 'value', 'date'])
    # print(df)
    df.to_csv("12-3.csv", index=False)


get_teams()
