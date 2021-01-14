# This file scrapes and gives scores
from bs4 import BeautifulSoup
import urllib
import sys
import requests
import operator
import datetime
import pandas as pd
import db_helper

cbs_link = "https://www.cbssports.com/college-basketball/teams/"

team_ratings = requests.get(cbs_link)
team_soup_ratings = BeautifulSoup(team_ratings.content, 'lxml')
team_table = team_soup_ratings.findAll(
    "span", {"class": "TeamName"})
for x in team_table:
    teamname1 = x.find('a').text
    if "-" in teamname1 or "(" in teamname1 or ")" in teamname1 or "." in teamname1:
        teamname1 = teamname1.replace("-", " ")
        teamname1 = teamname1.replace("(", "")
        teamname1 = teamname1.replace(")", "")
        teamname1 = teamname1.replace(".", "")
    print(teamname1)