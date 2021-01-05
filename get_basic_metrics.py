# This file scrapes and gives scores
from bs4 import BeautifulSoup
import urllib
import sys
import requests
import operator
import datetime
import pandas as pd


def add_ken_pom(teams_dict, KP):

    kenpom = requests.get(KP)
    soup_kenpom = BeautifulSoup(kenpom.content, 'lxml')
    kenpom_table = soup_kenpom.find("table", {"id": "ratings-table"})
    kenpom_table.findAll("tr")[2].findAll("td")[4]

    for x in kenpom_table.findAll("tr"):
        if x.find("a") == None or x.find("td") == None:
            pass
        else:
            team = x.find("a").text
            rank = int(x.find("td").text)
            val = x.findAll("td")[4].text
            # if "Merrimack" in team:
            #  continue
            teams_dict[team] = {}
            teams_dict[team]['Team'] = [team]
            teams_dict[team]['KenPomRank'] = rank
            teams_dict[team]['KenPomVal'] = val

# # This section adds BPI to the teams_dict


def add_BPI(teams_dict, BP):
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
                BPI_name = x.find("span", {"class": "team-names"}).text
                rank = x.findAll("td")[0].text
                val = x.findAll("td")[6].text
                if "Boston Univ." in team:
                    team = "Boston University"
                if "Long Island University" in team:
                    team = "LIU"
                if "Loyola (Chi)" in team:
                    team = "Loyola Chicago"
                if "Loyola (MD)" in team:
                    team = "Loyola MD"
                if "Arkansas St" in team:
                    team = "Arkansas State"
                if "Youngstown St" in team:
                    team = "Youngstown St."
                if "Tarleton" in team:
                    team = "Tarleton St."
                if "Savannah St" in team:
                    continue
                # if "Merrimack" in team:
                #  continue
                if "Umbc" in team:
                    team = "UMBC"
                if "-" in team or "(" in team or ")" in team:
                    team = team.replace("-", " ")
                    team = team.replace("(", "")
                    team = team.replace(")", "")
                if "é" in team:
                    team = team.replace("é", "e")
                if "NC St" in team:
                    team = team.replace("NC", "North Carolina")
                if "State" in team:
                    team = team.replace("State", "St.")
                if "CSU" in team:
                    team = team.replace("CSU", "Cal St.")
                if "CC" in team:
                    team = team.replace("CC", "Corpus Chris")
                if "Se " in team or "SE " in team or "Mt." in team:
                    team = team.replace("Se", "Southeast")
                    team = team.replace("SE", "Southeastern")
                    team = team.replace("Mt.", "Mount")
                if team in ["Seattle U", "UM Kansas City", "Arkansas Little Rock", "Appalachian St", "Georgia St", "North Carolina St.", "Southeastern Missouri St", "San José St", "South Carolina Upstate", "California Baptist", "Detroit Mercy", "McNeese", "Southeast Missouri St", "UT Martin", "Nicholls", "Grambling", "Miami", "Ole Miss", "UConn", "Pennsylvania", "UMass", "UL Monroe", "Omaha", "UIC", "Florida Int'l", "St. Francis BKN", "Hawai'i"]:
                    team = team.replace("Seattle U", "Seattle")
                    team = team.replace("UM Kansas City", "UMKC")
                    team = team.replace("Arkansas Little Rock", "Little Rock")
                    team = team.replace("Appalachian St", "Appalachian St.")
                    team = team.replace("Georgia St", "Georgia St.")
                    team = team.replace("North Carolina St.", "N.C. State")
                    team = team.replace("San José St", "San Jose St.")
                    team = team.replace(
                        "South Carolina Upstate", "USC Upstate")
                    team = team.replace("California Baptist", "Cal Baptist")
                    team = team.replace("Detroit Mercy", "Detroit")
                    team = team.replace("McNeese", "McNeese St.")
                    team = team.replace(
                        "Southeast Missouri St", "Southeast Missouri St.")
                    team = team.replace(
                        "Southeastern Missouri St", "Southeast Missouri St.")
                    team = team.replace("UT Martin", "Tennessee Martin")
                    team = team.replace("Nicholls", "Nicholls St.")
                    team = team.replace("Grambling", "Grambling St.")
                    team = team.replace("Miami", "Miami FL")
                    team = team.replace("Ole Miss", "Mississippi")
                    team = team.replace("UConn", "Connecticut")
                    team = team.replace("Pennsylvania", "Penn")
                    team = team.replace("UMass", "Massachusetts")
                    team = team.replace("UL Monroe", "Louisiana Monroe")
                    team = team.replace("Omaha", "Nebraska Omaha")
                    team = team.replace("UIC", "Illinois Chicago")
                    team = team.replace("Florida Int'l", "FIU")
                    team = team.replace("St. Francis BKN", "St. Francis NY")
                    team = team.replace("Hawai'i", "Hawaii")

                teams_dict[team]['BPIrank'] = rank
                teams_dict[team]['BPIval'] = val
                teams_dict[team]['Team'].append(BPI_name)

# #  This Section brings in SRS to teams


def add_sports_ref(teams_dict, SRS):
    srs = requests.get(SRS)
    soup_srs = BeautifulSoup(srs.content, 'lxml')
    srs_table = soup_srs.find("table", {"id": "ratings"})

    for x in srs_table.find("tbody").findAll("tr"):
        if x.find("a") == None:
            pass
        else:
            team = x.find("a").text
            SRS_name = x.find("a").text
            srs_val = x.findAll("td")[14].text
            o_eff = x.findAll("td")[15].text
            d_eff = x.findAll("td")[16].text
            ppg = x.findAll("td")[6].text
            papg = x.findAll("td")[7].text
            if "Savannah St" in team:
                continue
            # if "Merrimack" in team:
            #  continue
            if "State" in team:
                team = team.replace("State", "St.")
            if "University" in team:
                team = team.replace("University ", "")
            if "of " in team:
                team = team.replace("of ", "")
            if "-" in team or "(" in team or ")" in team:
                team = team.replace("-", " ")
                team = team.replace("(", "")
                team = team.replace(")", "")
            if team in ["Cal St. Long Beach", "North Carolina St.", "North Carolina Asheville", "South Carolina Upstate", "Albany NY", "Prairie View", "Missouri Kansas City", "Long Island University", "Massachusetts Lowell", "Maryland Baltimore County", "North Carolina Wilmington", "Saint Francis PA", "Grambling", "Central Connecticut St.", "Detroit Mercy", "Texas A&M Corpus Christi", "Omaha", "Texas Arlington", "Florida International", "California Baptist", "Bowling Green St.", "Texas San Antonio", "Texas Rio Grande Valley", "Texas El Paso", "Alabama Birmingham", "Southern Mississippi", "Citadel", "North Carolina Greensboro", "Southern Methodist", "Southern California", "Pennsylvania", "Nevada Las Vegas", "College Charleston", "St. John's NY", "Loyola IL", "Brigham Young", "Virginia Commonwealth", "Central Florida", "Louisiana St.", "Texas Christian", "Saint Mary's CA"]:
                team = team.replace("Cal St. Long Beach", "Long Beach St.")
                team = team.replace("North Carolina St.", "N.C. State")
                team = team.replace(
                    "North Carolina Asheville", "UNC Asheville")
                team = team.replace("South Carolina Upstate", "USC Upstate")
                team = team.replace("Albany NY", "Albany")
                team = team.replace("Prairie View", "Prairie View A&M")
                team = team.replace("Missouri Kansas City", "UMKC")
                team = team.replace("Long Island University", "LIU")
                team = team.replace("Massachusetts Lowell", "UMass Lowell")
                team = team.replace("Maryland Baltimore County", "UMBC")
                team = team.replace(
                    "North Carolina Wilmington", "UNC Wilmington")
                team = team.replace("Saint Francis PA", "St. Francis PA")
                team = team.replace("Grambling", "Grambling St.")
                team = team.replace(
                    "Central Connecticut St.", "Central Connecticut")
                team = team.replace("Detroit Mercy", "Detroit")
                team = team.replace(
                    "Texas A&M Corpus Christi", "Texas A&M Corpus Chris")
                team = team.replace("Omaha", "Nebraska Omaha")
                team = team.replace("Texas Arlington", "UT Arlington")
                team = team.replace("Florida International", "FIU")
                team = team.replace("California Baptist", "Cal Baptist")
                team = team.replace("Bowling Green St.", "Bowling Green")
                team = team.replace("Texas San Antonio", "UTSA")
                team = team.replace(
                    "Texas Rio Grande Valley", "UT Rio Grande Valley")
                team = team.replace("Texas El Paso", "UTEP")
                team = team.replace("Alabama Birmingham", "UAB")
                team = team.replace("Southern Mississippi", "Southern Miss")
                team = team.replace("Citadel", "The Citadel")
                team = team.replace(
                    "North Carolina Greensboro", "UNC Greensboro")
                team = team.replace("Southern Methodist", "SMU")
                team = team.replace("Southern California", "USC")
                team = team.replace("Pennsylvania", "Penn")
                team = team.replace("Nevada Las Vegas", "UNLV")
                team = team.replace("College Charleston", "Charleston")
                team = team.replace("St. John's NY", "St. John's")
                team = team.replace("Loyola IL", "Loyola Chicago")
                team = team.replace("Brigham Young", "BYU")
                team = team.replace("Virginia Commonwealth", "VCU")
                team = team.replace("Central Florida", "UCF")
                team = team.replace("Louisiana St.", "LSU")
                team = team.replace("Texas Christian", "TCU")
                team = team.replace("Saint Mary's CA", "Saint Mary's")

            teams_dict[team]['SRS'] = srs_val
            teams_dict[team]['o_eff'] = o_eff
            teams_dict[team]['d_eff'] = d_eff
            teams_dict[team]['ppg'] = ppg
            teams_dict[team]['papg'] = papg
            teams_dict[team]['Team'].append(SRS_name)


def add_advanced(teams_dict):
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
        if x.find("a") == None:
            pass
        else:
            team = x.find('a').text
            pace = x.findAll('td')[20].text
            Three_Par = x.findAll('td')[23].text
            TS = x.findAll('td')[24].text
            Tov = x.findAll('td')[30].text
            if "Savannah St" in team:
                continue
            # if "Merrimack" in team:
            #  continue
            if "State" in team:
                team = team.replace("State", "St.")
            if "University" in team:
                team = team.replace("University ", "")
            if "of " in team:
                team = team.replace("of ", "")
            if "-" in team or "(" in team or ")" in team:
                team = team.replace("-", " ")
                team = team.replace("(", "")
                team = team.replace(")", "")
            if team in ["North Carolina St.", "Cal St. Long Beach", "North Carolina Asheville", "South Carolina Upstate", "Albany NY", "Prairie View", "Missouri Kansas City", "Long Island University", "Massachusetts Lowell", "Maryland Baltimore County", "North Carolina Wilmington", "Saint Francis PA", "Grambling", "Central Connecticut St.", "Detroit Mercy", "Texas A&M Corpus Christi", "Omaha", "Texas Arlington", "Florida International", "California Baptist", "Bowling Green St.", "Texas San Antonio", "Texas Rio Grande Valley", "Texas El Paso", "Alabama Birmingham", "Southern Mississippi", "Citadel", "North Carolina Greensboro", "Southern Methodist", "Southern California", "Pennsylvania", "Nevada Las Vegas", "College Charleston", "St. John's NY", "Loyola IL", "Brigham Young", "Virginia Commonwealth", "Central Florida", "Louisiana St.", "Texas Christian", "Saint Mary's CA"]:
                team = team.replace("Cal St. Long Beach", "Long Beach St.")
                team = team.replace("North Carolina St.", "N.C. State")
                team = team.replace(
                    "North Carolina Asheville", "UNC Asheville")
                team = team.replace("South Carolina Upstate", "USC Upstate")
                team = team.replace("Albany NY", "Albany")
                team = team.replace("Prairie View", "Prairie View A&M")
                team = team.replace("Missouri Kansas City", "UMKC")
                team = team.replace("Long Island University", "LIU")
                team = team.replace("Massachusetts Lowell", "UMass Lowell")
                team = team.replace("Maryland Baltimore County", "UMBC")
                team = team.replace(
                    "North Carolina Wilmington", "UNC Wilmington")
                team = team.replace("Saint Francis PA", "St. Francis PA")
                team = team.replace("Grambling", "Grambling St.")
                team = team.replace(
                    "Central Connecticut St.", "Central Connecticut")
                team = team.replace("Detroit Mercy", "Detroit")
                team = team.replace(
                    "Texas A&M Corpus Christi", "Texas A&M Corpus Chris")
                team = team.replace("Omaha", "Nebraska Omaha")
                team = team.replace("Texas Arlington", "UT Arlington")
                team = team.replace("Florida International", "FIU")
                team = team.replace("California Baptist", "Cal Baptist")
                team = team.replace("Bowling Green St.", "Bowling Green")
                team = team.replace("Texas San Antonio", "UTSA")
                team = team.replace(
                    "Texas Rio Grande Valley", "UT Rio Grande Valley")
                team = team.replace("Texas El Paso", "UTEP")
                team = team.replace("Alabama Birmingham", "UAB")
                team = team.replace("Southern Mississippi", "Southern Miss")
                team = team.replace("Citadel", "The Citadel")
                team = team.replace(
                    "North Carolina Greensboro", "UNC Greensboro")
                team = team.replace("Southern Methodist", "SMU")
                team = team.replace("Southern California", "USC")
                team = team.replace("Pennsylvania", "Penn")
                team = team.replace("Nevada Las Vegas", "UNLV")
                team = team.replace("College Charleston", "Charleston")
                team = team.replace("St. John's NY", "St. John's")
                team = team.replace("Loyola IL", "Loyola Chicago")
                team = team.replace("Brigham Young", "BYU")
                team = team.replace("Virginia Commonwealth", "VCU")
                team = team.replace("Central Florida", "UCF")
                team = team.replace("Louisiana St.", "LSU")
                team = team.replace("Texas Christian", "TCU")
                team = team.replace("Saint Mary's CA", "Saint Mary's")

            teams_dict[team]['Pace'] = pace
            teams_dict[team]['Three_Par'] = Three_Par
            teams_dict[team]['True_Shoot'] = TS
            teams_dict[team]['Tov'] = Tov
    for x in opps:
        if x.find("a") == None or x.findAll("td")[16] == None:
            pass
        else:
            team = x.find('a').text
            pace = x.findAll('td')[20].text
            Three_Par = x.findAll('td')[23].text
            TS = x.findAll('td')[24].text
            Tov = x.findAll('td')[30].text

            if "Savannah St" in team:
                continue
            # if "Merrimack" in team:
            #  continue
            if "State" in team:
                team = team.replace("State", "St.")
            if "University" in team:
                team = team.replace("University ", "")
            if "of " in team:
                team = team.replace("of ", "")
            if "-" in team or "(" in team or ")" in team:
                team = team.replace("-", " ")
                team = team.replace("(", "")
                team = team.replace(")", "")
            if team in ["Cal St. Long Beach", "North Carolina St.", "North Carolina Asheville", "South Carolina Upstate", "Albany NY", "Prairie View", "Missouri Kansas City", "Long Island University", "Massachusetts Lowell", "Maryland Baltimore County", "North Carolina Wilmington", "Saint Francis PA", "Grambling", "Central Connecticut St.", "Detroit Mercy", "Texas A&M Corpus Christi", "Omaha", "Texas Arlington", "Florida International", "California Baptist", "Bowling Green St.", "Texas San Antonio", "Texas Rio Grande Valley", "Texas El Paso", "Alabama Birmingham", "Southern Mississippi", "Citadel", "North Carolina Greensboro", "Southern Methodist", "Southern California", "Pennsylvania", "Nevada Las Vegas", "College Charleston", "St. John's NY", "Loyola IL", "Brigham Young", "Virginia Commonwealth", "Central Florida", "Louisiana St.", "Texas Christian", "Saint Mary's CA"]:
                team = team.replace("Cal St. Long Beach", "Long Beach St.")
                team = team.replace("North Carolina St.", "N.C. State")
                team = team.replace(
                    "North Carolina Asheville", "UNC Asheville")
                team = team.replace("South Carolina Upstate", "USC Upstate")
                team = team.replace("Albany NY", "Albany")
                team = team.replace("Prairie View", "Prairie View A&M")
                team = team.replace("Missouri Kansas City", "UMKC")
                team = team.replace("Long Island University", "LIU")
                team = team.replace("Massachusetts Lowell", "UMass Lowell")
                team = team.replace("Maryland Baltimore County", "UMBC")
                team = team.replace(
                    "North Carolina Wilmington", "UNC Wilmington")
                team = team.replace("Saint Francis PA", "St. Francis PA")
                team = team.replace("Grambling", "Grambling St.")
                team = team.replace(
                    "Central Connecticut St.", "Central Connecticut")
                team = team.replace("Detroit Mercy", "Detroit")
                team = team.replace(
                    "Texas A&M Corpus Christi", "Texas A&M Corpus Chris")
                team = team.replace("Omaha", "Nebraska Omaha")
                team = team.replace("Texas Arlington", "UT Arlington")
                team = team.replace("Florida International", "FIU")
                team = team.replace("California Baptist", "Cal Baptist")
                team = team.replace("Bowling Green St.", "Bowling Green")
                team = team.replace("Texas San Antonio", "UTSA")
                team = team.replace(
                    "Texas Rio Grande Valley", "UT Rio Grande Valley")
                team = team.replace("Texas El Paso", "UTEP")
                team = team.replace("Alabama Birmingham", "UAB")
                team = team.replace("Southern Mississippi", "Southern Miss")
                team = team.replace("Citadel", "The Citadel")
                team = team.replace(
                    "North Carolina Greensboro", "UNC Greensboro")
                team = team.replace("Southern Methodist", "SMU")
                team = team.replace("Southern California", "USC")
                team = team.replace("Pennsylvania", "Penn")
                team = team.replace("Nevada Las Vegas", "UNLV")
                team = team.replace("College Charleston", "Charleston")
                team = team.replace("St. John's NY", "St. John's")
                team = team.replace("Loyola IL", "Loyola Chicago")
                team = team.replace("Brigham Young", "BYU")
                team = team.replace("Virginia Commonwealth", "VCU")
                team = team.replace("Central Florida", "UCF")
                team = team.replace("Louisiana St.", "LSU")
                team = team.replace("Texas Christian", "TCU")
                team = team.replace("Saint Mary's CA", "Saint Mary's")

            teams_dict[team]['Opp_Three_Par'] = Three_Par
            teams_dict[team]['Opp_True_Shoot'] = TS
            teams_dict[team]['Opp_Tov'] = Tov


def formatting(teams_dict):
    for x in teams_dict.keys():
        teams_dict[x]['record_date'] = datetime.datetime.now()
    teams_list = []
    sorted_teams_dict = sorted(teams_dict.items(), key=operator.itemgetter(0))
    for x, y in sorted_teams_dict:
        teams_list.append(y)
    return teams_list


def get_teams():
    teams = {}
    KP = 'https://kenpom.com/'
    BP = []
    for x in range(1, 16):
        BP.append(
            'http://www.espn.com/mens-college-basketball/bpi/_/view/bpi/page/' + str(x))
    SRS = "https://www.sports-reference.com/cbb/seasons/2021-ratings.html"

    add_ken_pom(teams, KP)
    add_sports_ref(teams, SRS)
    add_BPI(teams, BP)
    add_advanced(teams)

    teams = formatting(teams)
    print(len(teams))
    for x in teams:
        if len(x['Team']) < 3:
            teams.remove(x)
    print(len(teams))
    # for team in teams:
    #     print(team)
    # return teams
    df = pd.DataFrame(teams)
    df.to_csv("11-20.csv", index=False)


get_teams()
