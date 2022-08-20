from pybaseball import bwar_bat
from pybaseball import team_ids
from pybaseball import batting_stats
from pybaseball import playerid_reverse_lookup
from sqlalchemy import create_engine
import pandas as pd 
import warnings
import psycopg2
import time




def reverseLookup(mvp_awards): # Player Names based on bbref id
    player_names = playerid_reverse_lookup(mvp_awards['playerID'], key_type='bbref') # PyBaseball Function 
    player_names['Name'] = player_names['name_first'].map( # Create the Name Column
    lambda x: x.title()) + ' ' + player_names['name_last'].map(lambda x: x.title()) # Append first and last name
    player_names = player_names[['Name', 'key_bbref','mlb_played_first', 'mlb_played_last']] # Select columns

    return player_names.merge(mvp_awards, left_on= 'key_bbref', right_on='playerID').drop(['key_bbref'], axis=1)
          
   

                                                                                          
                                                                                          
def Merger(all_awards): # Preprocess MVP for Machine learning
    warnings.simplefilter("ignore")
    print('............Scraping Data.............\n')
    start_year, end_year, start_time = 1982, 2021, time.time()

    for i in range(end_year - start_year +1): # Loop through each Year
        current_year, year_time = start_year + i, time.time() # Define Current Year variable   

        if i < 1: # Base Case: at the start_year 
            data = getStats(current_year, all_awards) # Years Stats
            
            print(str(current_year)+' Time: '+str(time.time() - year_time)+' Seconds')
            
        else:
            new_data = getStats(current_year, all_awards) # Years Stats
            data = pd.concat([data, new_data]) # Combine old and new stats 
            
            complete_time = time.time() - year_time
            print(str(current_year)+' Time: '+str(complete_time)+' Seconds') if (i < 5) else print(
                '\n.....Approximately '+str(int((end_year - start_year +1)*(complete_time))
                                             )+'-'+str(int((end_year - start_year +1)*(complete_time)*1.25)
                                                  )+' Seconds.....\n') if (i==5) else False
    data = data.loc[data['Season']!=2020] # Drop Covid Season, Skewed Stats will affect Machine Learning
    print('Total Time: '+str(time.time() - start_time)+' Seconds')
    return data.loc[data['lgID']=='NL'], data.loc[data['lgID']=='AL']

def getStats(current_year, all_awards): # Years Stats
    data = mergeAwards(all_awards, current_year) # Get All Players and Awards
    return mvpChecker(data, current_year) # Find Players Awarded MVP

def mergeAwards(all_awards, current_year): # Find Awarded Players
    Players_Stats = batting_stats(str(current_year)).merge( # Pybaseball Scrapping Function
        all_awards.loc[all_awards['yearID'] == current_year]
                                                , how= 'left', left_on=['Name'], right_on=['Name']
    )
    Players_Stats['awardID'] = Players_Stats['awardID'].fillna('No Award') # Fill no award category
    teams_ids = team_ids(current_year)
    if current_year == 2021:
        teams_ids = team_ids(2020)
    AL_teams = teams_ids.loc[teams_ids['lgID']=='AL']
    NL_teams = teams_ids.loc[teams_ids['lgID']=='NL']
    teams_ids = {'Names':list(AL_teams['teamIDBR'])+list(NL_teams['teamIDBR']), 
                 'League':list(AL_teams['lgID'])+list(NL_teams['lgID'])}

    for i in range(len(Players_Stats)): # Loop over dataframe entries
        if list(Players_Stats['lgID'])[i] != 'AL' and list(Players_Stats['lgID'])[i] != 'NL': # If League not Clean
            for j in range(len(teams_ids['Names'])): # Loop over season teams
                if teams_ids['Names'][j] == list(Players_Stats['Team'])[i]: # If teams are the same
                    Players_Stats['lgID'][i] = teams_ids['League'][j] # Correct league  
        
    return Players_Stats.loc[Players_Stats['Team'] != '- - -'] # Return the cleaned data

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
    print('There are/is '+str(mvp_check['Name'].nunique())+' unique mvps over '+
         str(mvp_check['Season'].nunique())+' Seasons') # Print Unique Count
    print(mvp_check['Name'].unique()) # Print Unique Names
    return mvp_check