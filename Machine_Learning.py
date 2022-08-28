from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from pybaseball import batting_stats
from config import db_password
import pandas as pd
import sqlalchemy

def getData():
    engine = sqlalchemy.create_engine(f"postgresql://postgres:{db_password}@127.0.0.1:5432/Raw_Stats")
    data_NL=pd.read_sql_query('select * from "NL"',con=engine)
    data_AL=pd.read_sql_query('select * from "AL"',con=engine)
    return data_NL, data_AL

def preProcessing(data):
    selected_columns = [ 'Name','Age','G','AB','PA','H','1B','2B','3B','HR','R','RBI', # Keep Important Stats
                        'BB','IBB','SO','HBP','SF','SH','SB','AVG','OBP','SLG', 'OPS','ISO','BABIP','wOBA',
                        'wRAA','wRC','WAR','Spd','wRC+','WPA','-WPA','+WPA','RE24','REW','pLI','WPA/LI',
                        'Clutch','BsR','wSB','Off','AVG+','OBP+','SLG+','ISO+','BABIP+','MVP','XBH+']
    return data[selected_columns].dropna(
        axis=1).drop_duplicates().drop(['Name','Age'], axis=1) # Duplicate player entries based on Awards Recieved

def createLogisticRegression(data, leagueType):
    y = data['MVP'].values
    X = data.drop(['MVP'],axis=1).values
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    scaler = StandardScaler()
    X_scaler = scaler.fit(X_train)
    X_train_scaled = X_scaler.transform(X_train)
    X_test_scaled = X_scaler.transform(X_test)
    
    classifier = LogisticRegression(solver='lbfgs')
    classifier.fit(X_train_scaled, y_train) # Train the data
    y_pred = classifier.predict(X_test_scaled)
    print(accuracy_score(y_test, y_pred))
    
    
    
    current_year = batting_stats(2022, league=leagueType)
    current_year['MVP'] = 0
    current_year['XBH+'] =  (((current_year['R'] + current_year['2B'] + current_year[
        '3B'] + current_year['HR']) - (current_year['SO']))/current_year['PA'])
    
    selected_columns = [ 'Name','Age','G','AB','PA','H','1B','2B','3B','HR','R','RBI', # Keep Important Stats
                        'BB','IBB','SO','HBP','SF','SH','SB','AVG','OBP','SLG', 'OPS','ISO','BABIP','wOBA',
                        'wRAA','wRC','WAR','Spd','wRC+','WPA','-WPA','+WPA','RE24','REW','pLI','WPA/LI',
                        'Clutch','BsR','wSB','Off','AVG+','OBP+','SLG+','ISO+','BABIP+','MVP','XBH+']
    clean_current_year = current_year[selected_columns].drop(['Name','Age','MVP'], axis=1)
    realX = clean_current_year.values
    
    
    scaler = StandardScaler()
    X_scaler = scaler.fit(realX)
    X_test_scaled = X_scaler.transform(realX)
    pred_mvp_AL = classifier.predict(X_test_scaled)
    current_year['MVP']= pred_mvp_AL
    current_year['lgID']= leagueType.upper()
    return current_year


