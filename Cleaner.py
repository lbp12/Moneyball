from pybaseball import bwar_bat
from pybaseball import batting_stats_range
from pybaseball import playerid_reverse_lookup
from sqlalchemy import create_engine
import pandas as pd 
import psycopg2
import warnings
import time




def reverseLookup(mvp_awards): # Player Names based on bbref id
	player_names = playerid_reverse_lookup(mvp_awards['playerID'], key_type='bbref') # PyBaseball Function 
	player_names['Name'] = player_names['name_first'].map( # Create the Name Column
	lambda x: x.title()) + ' ' + player_names['name_last'].map(lambda x: x.title()) # Append first and last name
	player_names = player_names[['Name', 'key_bbref','mlb_played_first', 'mlb_played_last']] # Select columns

	return player_names.merge(mvp_awards, left_on= 'key_bbref', right_on='playerID').drop(['key_bbref'], axis=1)




def Merger(start_year, end_year, mvp_awards, all_awards, league_type): # Preprocess MVP for Machine learning
	seconds = time.time()
	war = bwar_bat() # Get war using Pybaseball function

	for i in range(end_year-start_year +1): # Loop through each Year
		current_year = start_year + i # Define Current Year variable
		if current_year = 2020: # Skip Covid, less games affects WAR
			current_year = current_year + 1

		if i < 1: # Base Case: at the start_year 
			data = getStats(current_year, mvp_awards, all_awards, war, league_type) # Years Stats

		else:
			new_data = getStats(current_year, mvp_awards, all_awards, war, league_type) # Years Stats
			data = pd.concat([data, new_data]) # Combine old and new stats 
			data['Tm'] = data['Tm'].map(lambda x: x.split(',')[-1]) # Most recent players team

	print(str(time.time()-seconds)+' Seconds')
	return data

def getStats(current_year, mvp_awards, all_awards, war, league_type): # Years Stats
	data = getPlayersYearStats(current_year, war, league_type) # Clean Player Stats
	mvpChecker(data, 'Name', mvp_awards, current_year, league_type) # Find Players Awarded MVP

	return addOtherStats(data, all_awards, current_year) # Find Awarded Players

def getPlayersYearStats(current_year, war, league_type): # Clean Player Stats
	war = war.loc[war['year_ID'] == current_year][['year_ID','name_common','WAR']] # Filter, Trim War
	batting_stats = batting_stats_range(str(current_year)+'-04-07', str(current_year)+'-10-05' # Pybaseball function
				       ).merge(war, how='left', left_on='Name', right_on='name_common' # Merge War
						      ).drop(['name_common', 'GDP','SH'], axis=1) # Drop unimportant columns
	batting_stats['Lev'] = batting_stats['Lev'].map(lambda x: x.split(',')[-1]) # Most recent players league

	return batting_stats.loc[batting_stats['Lev'] == league_type] # Retrieve Players from specified League

def mvpChecker(data, column, mvp_awards, current_year, league_type): # Find Players Awarded MVP
	for mvp in mvp_awards[column].loc[(mvp_awards['yearID'] == current_year) # Current Year's Awards
				      & (mvp_awards['lgID'] == league_type.split('-')[-1])]: # Cleaned most recent League
	data['MVP'] = data[column].map(lambda x: categorizer(mvp, x)) # Add MVP 
        
def addOtherStats(data, all_awards, current_year): # Find Awarded Players
	data = data.merge(all_awards.loc[ # Merge player data and all awards data
		all_awards['yearID'] == current_year][['Name','awardID'] # Based on current year and name
						     ], how='left', on='Name')
	data['awardID'] = data['awardID'].fillna('No Award') # Fill no award category
	data['WAR'] = data['WAR'].fillna(0) # Fill no war with average (Okay since less than 1/100 are null)

	return data # Return the cleaned data

def categorizer(mvp, player): # Assign 1 or 0 if MVP
        if mvp == player:
            return 1
        else:
            return 0
        
        
        
        
        
def mvpVerify(data): # Filter Data Frame To Check Work 
	mvp_check = data.loc[data['MVP'] == 1] 
	print('There are/is '+str(mvp_check['Name'].nunique())+' unique mvps') # Print Unique Count
	print(mvp_check['Name'].unique()) # Print Unique Names
	return mvp_check
