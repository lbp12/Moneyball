from pybaseball import bwar_bat
from pybaseball import batting_stats_range
from pybaseball import playerid_reverse_lookup
from sqlalchemy import create_engine
import pandas as pd 
import warnings
import time

def reverseLookup(mvp_awards):
    player_names = playerid_reverse_lookup(mvp_awards['playerID'], key_type='bbref')
    player_names['Name'] = player_names['name_first'].map(
        lambda x: x.title()) + ' ' + player_names['name_last'].map(lambda x: x.title())
    player_names = player_names[['Name', 'key_bbref','mlb_played_first', 'mlb_played_last']]
    
    return player_names.merge(mvp_awards, left_on= 'key_bbref', right_on='playerID').drop(['key_bbref'], axis=1)




def Merger(start_year, end_year, mvp_awards, all_awards, league_type):
    seconds = time.time()
    war = bwar_bat()  

    for i in range(end_year-start_year +1):
        current_year = start_year + i
        if i < 1:
            data = getStats(current_year, mvp_awards, all_awards, war, league_type)
            
        else:
            new_data = getStats(current_year, mvp_awards, all_awards, war, league_type)
            data = pd.concat([data, new_data])

    data['Tm'] = data['Tm'].map(lambda x: x.split(',')[-1])
    print(str(time.time()-seconds)+' Seconds')
    return data

def getStats(current_year, mvp_awards, all_awards, war, league_type):
    data = getPlayersYearStats(current_year, war, league_type)
    mvpChecker(data, 'Name', mvp_awards, current_year, league_type)
    
    return addOtherStats(data, all_awards, current_year)

def getPlayersYearStats(current_year, war, league_type):
    war = war.loc[war['year_ID'] == current_year][['year_ID','name_common','WAR']]
    batting_stats = batting_stats_range(str(current_year)+'-04-07', str(current_year)+'-10-05'
                                       ).merge(war, how='left', left_on='Name', right_on='name_common'
                                              ).drop(['name_common', 'GDP','SH'], axis=1)
    batting_stats['Lev'] = batting_stats['Lev'].map(lambda x: x.split(',')[-1])
    
    return batting_stats.loc[batting_stats['Lev'] == league_type]

def mvpChecker(data, column, mvp_awards, current_year, league_type):
    for mvp in mvp_awards[column].loc[(mvp_awards['yearID'] == current_year) 
                                      & (mvp_awards['lgID'] == league_type.split('-')[-1])]:
        data['MVP'] = data[column].map(lambda x: categorizer(mvp, x))
        
def addOtherStats(data, all_awards, current_year):
    data = data.merge(all_awards.loc[
        all_awards['yearID'] == current_year][['Name','awardID']
                                             ], how='left', on='Name')
    data['awardID'] = data['awardID'].fillna('No Award')
    data['WAR'] = data['WAR'].fillna(0)   
    
    return data

def categorizer(mvp, player):
        if mvp == player:
            return 1
        else:
            return 0
        
        
        
        
        
def mvpVerify(data):
    mvp_check = data.loc[data['MVP'] == 1]
    print('There are/is '+str(mvp_check['Name'].nunique())+' unique mvps')
    print(mvp_check['Name'].unique())
    return mvp_check