import json
import requests
import datetime as dt
import pickle
import pandas as pd
import mysql.connector
import os
from os.path import join, dirname
from datetime import date, datetime
from dotenv import load_dotenv
import db_helper

def get_odds_data():
    api_key = 'da3195c8356b3b0ee3e5a6682ed9c537'
    sports_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
        'api_key': api_key,
        'sport': 'basketball_ncaab',
        'region': 'us',
        'oddsFormat': 'american'
    })


#     print(sports_response.headers['x-requests-remaining'])
    sports_json = json.loads(sports_response.text)
    return sports_json
    
def getTeamData(teamid):
    teamid = teamid.replace(" ", "%20")
    baseUrl="https://fastbreakstats-server-main-hqc7w3njda-uc.a.run.app/teams/"
    url=baseUrl+teamid

    r = requests.get(url = url).json()
    bpival = r['bpi']
    kpval = r['kp']
    srsval = r['srs']
    return kpval, bpival, srsval

def get_needed_odds(conf):
    #This function calculates the odds needed for a bet to have an expected value of .1
    #An EV of .1 means a $.10 expected return on $1 over time
    #The normal formula is EV = (payout * confidence) - (bet * (1-conf))
    #payout is the expected profit on a bet.
    #confidence is models % chance of winning. 1-conf is for the other team
    #The bet is always going to be $1 for simple math which removes the need for the bet variable
    #below equation is rearranged to isolate and solve for the payout
    payout = round(((.1+(1-conf))/conf),4) 
    #convert payout to american odds
    if 100/payout > 100:
        odds = round(-100/payout)
    else:
        odds = round(100*payout)
    return odds

def get_ev(odds,conf):
    #This calculates the Expected Return on a $1 bet with the actual given bookie odds we pass in
    #EV of .1 means a 10 cent return on a $1 bet over time
    if int(odds) > 0:
        payout = odds/100
    else:
        payout = -100/odds
    ev = (conf * payout) - (1-conf)
    return ev

def get_kelly_bet(odds,conf):
    if int(odds) > 0:
        dec = 1+(odds/100)
    else:
        dec = 1-(100/odds)
    kb = ((dec*conf) - (1-conf))/dec
    return kb

def convert_epoch(epoch):
    return dt.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:00')

def get_best_bets(teams,loaded_model,sports_json):
    games_to_bet = []
    for game in sports_json['data']:
        #Loop through and get odds
        if game['commence_time'] < dt.datetime.now().timestamp():
            continue
        if dt.datetime.fromtimestamp(game['commence_time']).date() > dt.datetime.now().date():
            continue

        game_time = convert_epoch(game['commence_time'])
        home = game['home_team']
        if game['home_team'] == game['teams'][0]:
            away = game['teams'][1]
        else:
            away = game['teams'][0]

        try:
            home = home.replace("-", " ")
            home = home.replace("(", "")
            home = home.replace(")", "")
            home = home.replace(".", "")
            away = away.replace("-", " ")
            away = away.replace("(", "")
            away = away.replace(")", "")
            away = away.replace(".", "")
            homeid = str(teams.loc[teams['odds_api_name'] == home]['teamID'].values[0])
            awayid = str(teams.loc[teams['odds_api_name'] == away]['teamID'].values[0])
            homekp, homebpi, homesrs = getTeamData(homeid)
            awaykp, awaybpi, awaysrs = getTeamData(awayid)
        except Exception as e:
            print(e)
            print(game['teams'])
            continue

        res = loaded_model.predict_proba([[float(awaykp), float(awaybpi), float(awaysrs), float(homekp), float(homebpi), float(homesrs)]])
        away_needed_odds = int(get_needed_odds(res[0][0]))    
        home_needed_odds = int(get_needed_odds(res[0][1]))

    #     print()
        sites = list(filter(lambda site: site['site_key'] in ['williamhill_us','draftkings','bovada'], game['sites']))
        if not sites:
    #         print("Empty")
            continue
    #     print(game['teams'],game['home_team'])
        site_list, update_time_list, home_odds, away_odds = [],[],[],[]
        for site in sites:
            site_list.append(site['site_key'])
            update_time_list.append(convert_epoch(site['last_update']))
            if home == game['teams'][0]:
                home_odds.append(int(site['odds']['h2h'][0]))
                away_odds.append(int(site['odds']['h2h'][1]))
            else:
                home_odds.append(int(site['odds']['h2h'][1]))
                away_odds.append(int(site['odds']['h2h'][0]))


    #     print("Game Time:", game_time)
    #     print('Home team:', homeid)
    #     print('Away team:', awayid)
#         print('Home needed odds:', home_needed_odds)
#         print('Away needed odds:', away_needed_odds)
    #     print('Sites to check:', site_list)
    #     print('Last Updated:', update_time_list)
    #     print('Home Odds', home_odds)
    #     print('Away Odds', away_odds)
    #     print()

        if any(home_odd > home_needed_odds for home_odd in home_odds):
            index = home_odds.index(max(home_odds))
    #         print('Sites to check:', site_list[index])
    #         print('Last Updated:', update_time_list[index])
    #         print('Betting Odds', home_odds[index])
    #         print('Team to Bet ID', homeid)
            game_to_bet = []
            game_to_bet.append(game_time)
            game_to_bet.append(str(homeid))
            game_to_bet.append(str(awayid))
            game_to_bet.append(site_list[index])
            game_to_bet.append(str(home_odds[index]))
            game_to_bet.append(update_time_list[index])
            game_to_bet.append(str(home_needed_odds))
            game_to_bet.append(str(homeid))
            games_to_bet.append(game_to_bet)
        if any(away_odd > away_needed_odds for away_odd in away_odds):
            index = away_odds.index(max(away_odds))
    #         print('Best Site for bet:', site_list[index])
    #         print('Last Updated:', update_time_list[index])
    #         print('Odds', away_odds[index])
    #         print('Team to Bet ID', awayid)
            game_to_bet = []
            game_to_bet.append(game_time)
            game_to_bet.append(str(homeid))
            game_to_bet.append(str(awayid))
            game_to_bet.append(site_list[index])
            game_to_bet.append(str(away_odds[index]))
            game_to_bet.append(update_time_list[index])
            game_to_bet.append(str(away_needed_odds))
            game_to_bet.append(str(awayid))
            games_to_bet.append(game_to_bet)
    return games_to_bet

def get_all_good_odds(teams,loaded_model,sports_json):
    games_to_bet = []
    for game in sports_json['data']:
        #Loop through and get odds
        if game['commence_time'] < dt.datetime.now().timestamp():
            continue
        if dt.datetime.fromtimestamp(game['commence_time']).date() > dt.datetime.now().date():
            continue

        game_time = convert_epoch(game['commence_time'])
        home = game['home_team']
        if game['home_team'] == game['teams'][0]:
            away = game['teams'][1]
        else:
            away = game['teams'][0]

        try:
            home = home.replace("-", " ")
            home = home.replace("(", "")
            home = home.replace(")", "")
            home = home.replace(".", "")
            away = away.replace("-", " ")
            away = away.replace("(", "")
            away = away.replace(")", "")
            away = away.replace(".", "")
            homeid = str(teams.loc[teams['odds_api_name'] == home]['teamID'].values[0])
            awayid = str(teams.loc[teams['odds_api_name'] == away]['teamID'].values[0])
            homekp, homebpi, homesrs = getTeamData(homeid)
            awaykp, awaybpi, awaysrs = getTeamData(awayid)
        except Exception as e:
            print(e)
            print(game['teams'])
            continue

        res = loaded_model.predict_proba([[float(awaykp), float(awaybpi), float(awaysrs), float(homekp), float(homebpi), float(homesrs)]])
        away_needed_odds = int(get_needed_odds(res[0][0]))    
        home_needed_odds = int(get_needed_odds(res[0][1]))

        #site,odds,update,ev
        bovada = ['bovada',None,None]
        draftkings = ['dk',None,None]
        willhill = ['wh',None,None]
    #     print()
        sites = list(filter(lambda site: site['site_key'] in ['williamhill_us','draftkings','bovada'], game['sites']))
    #     print(sites)
        if not sites:
            continue
        for site in sites:
            if site['site_key'] == 'williamhill_us':
                willhill[2] = convert_epoch(site['last_update'])
                if home == game['teams'][0]:
                    home_odds = int(site['odds']['h2h'][0])
                    away_odds = int(site['odds']['h2h'][1])
                else:
                    home_odds = int(site['odds']['h2h'][1])
                    away_odds = int(site['odds']['h2h'][0])
                if home_odds > home_needed_odds:
                    willhill[1] = home_odds
                    single_needed_odds = home_needed_odds
                    team_to_bet = homeid
#                     willhill[3] = round(get_ev(home_odds,res[0][1]),2)
                if away_odds > away_needed_odds:
                    willhill[1] = away_odds
                    single_needed_odds = away_needed_odds
                    team_to_bet = awayid
#                     willhill[3] = round(get_ev(away_odds,res[0][0]),2)
            elif site['site_key'] == 'draftkings':
                draftkings[2] = convert_epoch(site['last_update'])
                if home == game['teams'][0]:
                    home_odds = int(site['odds']['h2h'][0])
                    away_odds = int(site['odds']['h2h'][1])
                else:
                    home_odds = int(site['odds']['h2h'][1])
                    away_odds = int(site['odds']['h2h'][0])
                if home_odds > home_needed_odds:
                    draftkings[1] = home_odds
                    single_needed_odds = home_needed_odds
                    team_to_bet = homeid
#                     draftkings[3] = round(get_ev1(home_odds,res[0][1]),2)
                if away_odds > away_needed_odds:
                    draftkings[1] = away_odds
                    single_needed_odds = away_needed_odds
                    team_to_bet = awayid
#                     draftkings[3] = round(get_ev1(away_odds,res[0][0]),2)
            elif site['site_key'] == 'bovada':
                bovada[2] = convert_epoch(site['last_update'])
                if home == game['teams'][0]:
                    home_odds = int(site['odds']['h2h'][0])
                    away_odds = int(site['odds']['h2h'][1])
                else:
                    home_odds = int(site['odds']['h2h'][1])
                    away_odds = int(site['odds']['h2h'][0])
                if home_odds > home_needed_odds:
                    bovada[1] = home_odds
                    single_needed_odds = home_needed_odds
                    team_to_bet = homeid
#                     bovada[3] = round(get_ev1(home_odds,res[0][1]),2)
                if away_odds > away_needed_odds:
                    bovada[1] = away_odds
                    single_needed_odds = away_needed_odds
                    team_to_bet = awayid
#                     bovada[3] = round(get_ev1(away_odds,res[0][0]),2)

        if bovada[1] or draftkings[1] or willhill[1]:
    #         print(game['teams'],game['home_team'])
    #         print("Game Time:", game_time)
    #         print('Home team:', homeid)
    #         print('Away team:', awayid)
    #         print('Team to bet:', team_to_bet)
    #         print('Needed odds:', single_needed_odds)
    #         print(bovada)
    #         print(draftkings)
    #         print(willhill)
            game_to_bet = []
            game_to_bet.append(game_time)
            game_to_bet.append(str(homeid))
            game_to_bet.append(str(awayid))
            game_to_bet.append(str(bovada[1]))
            game_to_bet.append(str(draftkings[1]))
            game_to_bet.append(str(willhill[1]))
            game_to_bet.append(bovada[2])
            game_to_bet.append(draftkings[2])
            game_to_bet.append(willhill[2])
            game_to_bet.append(str(single_needed_odds))
            game_to_bet.append(str(team_to_bet))
            
            games_to_bet.append(game_to_bet)
        else:
            continue

    return games_to_bet

def main():
    url="https://fastbreakstats-server-main-hqc7w3njda-uc.a.run.app/teams"
    r = requests.get(url = url).json()
    teams = pd.DataFrame(r)
    loaded_model = pickle.load(open('6yr_LR.sav', 'rb'))
    # games_to_bet = []
    sports_json = get_odds_data()

    best_bets = get_best_bets(teams,loaded_model,sports_json)
    good_odds = get_all_good_odds(teams,loaded_model,sports_json)

    db = db_helper.Db_Helper()
    db.insert_odds_historical(best_bets)
    db.insert_odds(good_odds)
    db.close()

main()
