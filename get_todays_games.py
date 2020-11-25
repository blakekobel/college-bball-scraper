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
    print(sref_table)
    for x in sref_table:
        # .has_attr('href'):
        if x.find("tbody").findAll("tr")[0].find("a") and x.find("tbody").findAll("tr")[1].find("a"):
            teamname1 = x.find("tbody").findAll("tr")[0].find("a").text
            teamname2 = x.find("tbody").findAll("tr")[1].find("a").text
            if teamname1 in ['UCSB', "St. Peter's", "St. Joseph's", "BYU", "Saint Mary's", 'UMKC', 'SIU-Edwardsville', 'UTSA', 'UT-Martin', 'UTEP', 'LSU', 'California', 'Penn', 'USC', 'Southern Miss', 'LIU-Brooklyn', 'TCU', 'ETSU', 'Central Connecticut', 'Pitt', 'Detroit', 'Ole Miss', 'UIC', 'UNC', 'NC State', 'USC Upstate', 'UMBC', 'UMass', 'UMass-Lowell', 'UNC Asheville', 'UConn', 'VCU', 'SMU', 'UCF', 'UNLV', 'UNC Wilmington', 'UNC Greensboro']:
                teamname1 = teamname1.replace(
                    "UNC Asheville", "North Carolina-Asheville")
                teamname1 = teamname1.replace(
                    "UNC Wilmington", "North Carolina-Wilmington")
                teamname1 = teamname1.replace(
                    "UNC Greensboro", "North Carolina-Greensboro")
                teamname1 = teamname1.replace("UNC", "North Carolina")
                teamname1 = teamname1.replace(
                    "NC State", "North Carolina State")
                teamname1 = teamname1.replace(
                    "USC Upstate", "South Carolina Upstate")
                teamname1 = teamname1.replace(
                    "UMBC", "Maryland-Baltimore County")
                teamname1 = teamname1.replace("UMass", "Massachusetts")
                teamname1 = teamname1.replace("UConn", "Connecticut")
                teamname1 = teamname1.replace("VCU", "Virginia Commonwealth")
                teamname1 = teamname1.replace("SMU", "Southern Methodist")
                teamname1 = teamname1.replace("UCF", "Central Florida")
                teamname1 = teamname1.replace("UNLV", "Nevada-Las Vegas")
                teamname1 = teamname1.replace("UIC", "Illinois-Chicago")
                teamname1 = teamname1.replace("Ole Miss", "Mississippi")
                teamname1 = teamname1.replace("Detroit", "Detroit Mercy")
                teamname1 = teamname1.replace("Pitt", "Pittsburgh")
                teamname1 = teamname1.replace(
                    "Central Connecticut", "Central Connecticut State")
                teamname1 = teamname1.replace("ETSU", "East Tennessee State")
                teamname1 = teamname1.replace("TCU", "Texas Christian")
                teamname1 = teamname1.replace(
                    "LIU-Brooklyn", "Long Island University")
                teamname1 = teamname1.replace(
                    "Southern Miss", "Southern Mississippi")
                teamname1 = teamname1.replace(
                    "California", "University of California")
                teamname1 = teamname1.replace("USC", "Southern California")
                teamname1 = teamname1.replace("Penn", "Pennsylvania")
                teamname1 = teamname1.replace("LSU", "Louisiana State")
                teamname1 = teamname1.replace("UTEP", "Texas-El Paso")
                teamname1 = teamname1.replace("UT-Martin", "Tennessee-Martin")
                teamname1 = teamname1.replace("UTSA", "Texas-San Antonio")
                teamname1 = teamname1.replace(
                    "SIU-Edwardsville", "SIU Edwardsville")
                teamname1 = teamname1.replace("UMKC", "Missouri-Kansas City")
                teamname1 = teamname1.replace(
                    "Saint Mary's", "Saint Mary's (CA)")
                teamname1 = teamname1.replace("BYU", "Brigham Young")
                teamname1 = teamname1.replace("St. Joseph's", "Saint Joseph's")
                teamname1 = teamname1.replace("St. Peter's", "Saint Peter's")
                teamname1 = teamname1.replace("UCSB", "UC-Santa Barbara")

            if teamname2 in ['UCSB', "St. Peter's", "St. Joseph's", "BYU", "Saint Mary's", 'UMKC', 'SIU-Edwardsville', 'UTSA', 'UT-Martin', 'UTEP', 'LSU', 'California', 'Penn', 'USC', 'Southern Miss', 'LIU-Brooklyn', 'TCU', 'ETSU', 'Central Connecticut', 'Pitt', 'Detroit', 'Ole Miss', 'UIC', 'UNC', 'NC State', 'USC Upstate', 'UMBC', 'UMass', 'UMass-Lowell', 'UNC Asheville', 'UConn', 'VCU', 'SMU', 'UCF', 'UNLV', 'UNC Wilmington', 'UNC Greensboro']:
                teamname2 = teamname2.replace(
                    "UNC Asheville", "North Carolina-Asheville")
                teamname2 = teamname2.replace(
                    "UNC Wilmington", "North Carolina-Wilmington")
                teamname2 = teamname2.replace(
                    "UNC Greensboro", "North Carolina-Greensboro")
                teamname2 = teamname2.replace("UNC", "North Carolina")
                teamname2 = teamname2.replace(
                    "NC State", "North Carolina State")
                teamname2 = teamname2.replace(
                    "USC Upstate", "South Carolina Upstate")
                teamname2 = teamname2.replace(
                    "UMBC", "Maryland-Baltimore County")
                teamname2 = teamname2.replace("UMass", "Massachusetts")
                teamname2 = teamname2.replace("UConn", "Connecticut")
                teamname2 = teamname2.replace("VCU", "Virginia Commonwealth")
                teamname2 = teamname2.replace("SMU", "Southern Methodist")
                teamname2 = teamname2.replace("UCF", "Central Florida")
                teamname2 = teamname2.replace("UNLV", "Nevada-Las Vegas")
                teamname2 = teamname2.replace("UIC", "Illinois-Chicago")
                teamname2 = teamname2.replace("Ole Miss", "Mississippi")
                teamname2 = teamname2.replace("Detroit", "Detroit Mercy")
                teamname2 = teamname2.replace("Pitt", "Pittsburgh")
                teamname2 = teamname2.replace(
                    "Central Connecticut", "Central Connecticut State")
                teamname2 = teamname2.replace("ETSU", "East Tennessee State")
                teamname2 = teamname2.replace("TCU", "Texas Christian")
                teamname2 = teamname2.replace(
                    "LIU-Brooklyn", "Long Island University")
                teamname2 = teamname2.replace(
                    "Southern Miss", "Southern Mississippi")
                teamname2 = teamname2.replace(
                    "California", "University of California")
                teamname2 = teamname2.replace("USC", "Southern California")
                teamname2 = teamname2.replace("Penn", "Pennsylvania")
                teamname2 = teamname2.replace("LSU", "Louisiana State")
                teamname2 = teamname2.replace("UTEP", "Texas-El Paso")
                teamname2 = teamname2.replace("UT-Martin", "Tennessee-Martin")
                teamname2 = teamname2.replace("UTSA", "Texas-San Antonio")
                teamname2 = teamname2.replace(
                    "SIU-Edwardsville", "SIU Edwardsville")
                teamname2 = teamname2.replace("UMKC", "Missouri-Kansas City")
                teamname2 = teamname2.replace(
                    "Saint Mary's", "Saint Mary's (CA)")
                teamname2 = teamname2.replace("BYU", "Brigham Young")
                teamname2 = teamname2.replace("St. Joseph's", "Saint Joseph's")
                teamname2 = teamname2.replace("St. Peter's", "Saint Peter's")
                teamname2 = teamname2.replace("UCSB", "UC-Santa Barbara")

            game_list.append((teamname1, teamname2))
        else:
            pass

    print(game_list)


scrape_games()
