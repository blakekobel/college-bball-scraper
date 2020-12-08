import os
import pandas as pd
import db_helper

def scrape(request):
    db = db_helper.Db_Helper()

    teams = db.get_teams()
    df = pd.DataFrame(teams, columns=['id','kenpom_name','sr_name','bpi_name','extra_name1','extra_name2','extra_name3'])
    print(df)

scrape("request")