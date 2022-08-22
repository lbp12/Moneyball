from pybaseball import bwar_bat
from pybaseball import team_ids
from pybaseball import batting_stats
from pybaseball import playerid_lookup
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
            
    id_list = []
    for i in range(len(player_names['name_first'])):
        id_list.append(playerid_lookup(player_names['name_first'][i], player_names['name_last'][i]))
    player_names['IDfg'] = id_list
    player_names = player_names[['key_fangraphs','Name', 'key_bbref']] # Select columns
    
    return player_names.merge(mvp_awards, left_on= 'key_bbref', right_on='playerID'
                             ).drop(['key_bbref','tie','notes'], axis=1)
          
   

                                                                                          
                                                                                          
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
            printStatement(start_year, end_year, year_time, i)

    return finalProcessing(data, start_time)

def getStats(current_year, all_awards): # Years Stats
    data = mergeAwards(all_awards, current_year) # Get All Players and Awards
    
    return mvpChecker(data, current_year) # Find Players Awarded MVP

def mergeAwards(all_awards, current_year): # Find Awarded Players
    Players_Stats = batting_stats(str(current_year)).merge( # Pybaseball Scrapping Function
        all_awards.loc[all_awards['yearID'] == current_year].drop(['Name'], axis=1)
                                                , how= 'left', left_on=['IDfg'], right_on=['key_fangraphs']
    )
    Players_Stats['awardID'] = Players_Stats['awardID'].fillna('No Award') # Fill no award category
    teams_ids = team_ids(current_year)
    if current_year == 2021: # Team names do not exist past 2020, replace with 2020
        teams_ids = team_ids(2020)
        
    Teams = {'- - -':'ML'} # Start Hashing
    for i in range(len(teams_ids['teamIDBR'])): # Loop over seasons teams add to Hashmap
        Teams[list(teams_ids['teamIDBR'])[i]] = str(list(teams_ids['lgID'])[i])

    for i in range(len(Players_Stats)): # Loop over dataframe entries
        if list(Players_Stats['lgID'])[i] != 'AL' and list(Players_Stats['lgID'])[i] != 'NL': # If League not Clean
            Players_Stats['lgID'][i] = Teams[list(Players_Stats['Team'])[i]] # Get Hashmaps value
        
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
        
def printStatement(start_year, end_year, year_time, i): # Lets user know Approximate time
    complete_time = time.time() - year_time
    print(str(start_year + i)+' Time: '+str(complete_time)+' Seconds') if (i < 5) else print(
        '\n.....Approximately '+str(int((end_year - start_year +1)*(complete_time))
                                   )+'-'+str(int((end_year - start_year +1)*(complete_time)*1.25)
                                            )+' Seconds.....\n') if (i==5) else False

def finalProcessing(data, start_time):
    data = data.loc[data['Season']!=2020] # Drop Covid Season, Skewed Stats will affect Machine Learning
    print('Total Time: '+str(time.time() - start_time)+' Seconds')
    data_NL = data.loc[(data['lgID']=='NL')]
    data_AL = data.loc[data['lgID']=='AL']
    
    return data_NL[(data_NL['Season'] != 2014) # Drop Season where pitchers won
                  ] , data_AL[~data_AL['Season'].isin([1984, 1986, 1992, 2011])]
            
            
            
     
                                                                                          
def mvpVerify(data, all_awards, leagueType): # Filter Data Frame To Check Work 
    new = all_awards.loc[(all_awards['awardID']=='Most Valuable Player') &
              (all_awards['lgID']==leagueType)].sort_values(by = ['yearID']).tail(40)
    actual_mvps = new['Name'].unique()
    print(str(len(actual_mvps))+' Total, minus:')
    print('Freddie Freeman and Clayton Kershaw\n\n') if (leagueType=='NL') else print(
        'Justin Verlander, Roger Clemens, José Abreu, Willie Hernandez, Ken Griffey, Dennis Eckersley\n\n')
    
    mvp_check = data.loc[data['MVP'] == 1] 
    print('There are/is '+str(mvp_check['Name'].nunique())+' unique mvps over '+
         str(mvp_check['Season'].nunique())+' Seasons\n') # Print Unique Count
    found_mvps = [mvp.title() for mvp in list(mvp_check['Name'].unique())]
    print("Skipped MVP's:")
    print(set(actual_mvps).difference(found_mvps)) # Missed Names
    
    return mvp_check