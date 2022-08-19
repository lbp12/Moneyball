from pybaseball import bwar_bat
from pybaseball import batting_stats
from pybaseball import playerid_reverse_lookup
from sqlalchemy import create_engine
import pandas as pd 
import psycopg2
import time




def reverseLookup(mvp_awards): # Player Names based on bbref id
    player_names = playerid_reverse_lookup(mvp_awards['playerID'], key_type='bbref') # PyBaseball Function 
    player_names['Name'] = player_names['name_first'].map( # Create the Name Column
    lambda x: x.title()) + ' ' + player_names['name_last'].map(lambda x: x.title()) # Append first and last name
    player_names = player_names[['Name', 'key_bbref','mlb_played_first', 'mlb_played_last']] # Select columns

    return player_names.merge(mvp_awards, left_on= 'key_bbref', right_on='playerID').drop(['key_bbref'], axis=1)
          
   
                                                                                          
                                                                                          
def Merger(all_awards): # Preprocess MVP for Machine learning
    print('.............Scrapping Data............\n')
    start_year, end_year, start_time = 2008, 2021, time.time()

    for i in range(end_year - start_year +1): # Loop through each Year
        current_year, year_time = start_year + i, time.time() # Define Current Year variable   
        if current_year == 2020: # Add 2021 stats to COVID year, less games affected recorded stats
            current_year = current_year + 1

        if i < 1: # Base Case: at the start_year 
            data = getStats(current_year, all_awards) # Years Stats
            print(str(current_year)+' Time: '+str(time.time() - year_time)+' Seconds')
            
        else:
            new_data = getStats(current_year, all_awards) # Years Stats
            data = pd.concat([data, new_data]) # Combine old and new stats 
            print(str(current_year)+' Time: '+str(
                time.time() - year_time)+' Seconds') if (i < 5) else print(
                '\n............Just A Moment................\n') if (i==5) else False

    print('Total Time: '+str(time.time() - start_time)+' Seconds')
    return data

def getStats(current_year, all_awards): # Years Stats
    data = mergeAwards(all_awards, current_year) # Get All Players and Awards
    return mvpChecker(data, current_year) # Find Players Awarded MVP

def mergeAwards(all_awards, current_year): # Find Awarded Players
    Players_Stats = batting_stats(str(current_year)).merge( # Pybaseball Scrapping Function
        all_awards.loc[all_awards['yearID'] == current_year]
                                                , how= 'left', left_on=['Name'], right_on=['Name']
    )
    Players_Stats['awardID'] = Players_Stats['awardID'].fillna('No Award') # Fill no award category
    return Players_Stats # Return the cleaned data

def mvpChecker(data, current_year): # Find Players Awarded MVP
    mvp_list = list(data.loc[
        (data['awardID'] == 'Most Valuable Player')&
        (data['Season'] == current_year)]['Name'])
    data['MVP'] = data['Name'].map(lambda x: categorizer(mvp_list, x)) # Add MVP 
    return data

def categorizer(mvp_list, player): # Assign 1 or 0 if MVP
        if (player in mvp_list):
            return 1
        else:
            return 0                                                                                          
                                                                                          
                                                                                          
        
                                                                                          
def mvpVerify(data): # Filter Data Frame To Check Work 
    mvp_check = data.loc[data['MVP'] == 1] 
    print('There are/is '+str(mvp_check['Name'].nunique())+' unique mvps') # Print Unique Count
    print(mvp_check['Name'].unique()) # Print Unique Names
    return mvp_check