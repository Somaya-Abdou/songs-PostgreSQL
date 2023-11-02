import pandas as pd 
import psycopg2
import configparser
import sql 

class create_database :
    config = configparser.ConfigParser()
    config.read('login.cfg')
    host = config.get('DataBase', 'host')
    dbname = config.get('DataBase','dbname')
    user = config.get('DataBase', 'user')
    password = config.get('DataBase','password')
    
    def __init__ (self,create_database,drop_database):
        self.__create_database = create_database
        self.__drop_database  = drop_database

    def create_database (self):
    #setting up postgres connection
        conn = psycopg2.connect(f"host={create_database.host} dbname={create_database.dbname}\
                                 user={create_database.user} password={create_database.password}")
        cur = conn.cursor()
        conn.set_session(autocommit=True)
    
    #creating database
        cur.execute(self.__drop_database)
        cur.execute(self.__create_database)
        conn.close()

    #connecting to the database
        conn = psycopg2.connect(f"host={create_database.host} dbname=songs user={create_database.user}\
                                 password={create_database.password}")
        conn.set_session(autocommit=True)     
        cur = conn.cursor()
        return(cur,conn)

def drop_tables (cur,drop_tables):
    for table in drop_tables :
        cur.execute(table)

def create_tables (cur,create_tables):    
    for table in create_tables :
        cur.execute(table)

         
def insert_into_tables (df,df2,insert_into_tables,cur):
    df.drop(index = 30632,inplace=True)
    df.drop(columns = ['key','mode','tempo','valence'],axis = 1,inplace = True)
    df.reset_index(inplace=True)

    #inserting into general_table
    df_general_table = df[['spotify_id','name','artists','album_name','country','is_explicit']]
    for index , row in df_general_table.iterrows() :
        cur.execute(insert_into_tables[0],row)
    
    #inserting into rating_table
    df_rating_table = df[['index','spotify_id','daily_rank','daily_movement','weekly_movement','popularity']]
    for index , row in df_rating_table.iterrows() :
        cur.execute(insert_into_tables[1],row)
    
    #inserting into time table
    duration_min = df['duration_ms'].div(36000).tolist()
    album_release_day = pd.to_datetime(df['album_release_date']).dt.day.tolist()
    album_release_month = pd.to_datetime(df['album_release_date']).dt.month.tolist()
    album_release_year = pd.to_datetime(df['album_release_date']).dt.year.tolist()
    columns = ['spotify_id','duration_min','album_release_day','album_release_month','album_release_year','time_signature']
    df_time_table = pd.DataFrame(list(zip(df['spotify_id'].tolist(),duration_min,album_release_day,\
                                          album_release_month,album_release_year,df['time_signature'].tolist())),\
                                          columns = columns)
    for index , row in df_time_table.iterrows() :
        cur.execute(insert_into_tables[2],row)

    #inserting into song_decription_table 
    df_song_decription_table = df[['spotify_id','danceability','energy','loudness',\
                                   'speechiness','acousticness','instrumentalness','liveness']]
    for index , row in df_song_decription_table.iterrows() :
        cur.execute(insert_into_tables[3],row) 

    #inserting into country_table 
    for index , row in df2.iterrows() :
        cur.execute(insert_into_tables[4],row)
    
df = pd.read_csv('universal_top_spotify_songs.csv',delimiter=',')
df2 = pd.read_csv('country.csv',delimiter=',') 
cur,conn = create_database(sql.create_database,sql.drop_database).create_database()
drop_tables(cur,sql.drop_tables)
create_tables(cur,sql.create_tables)
insert_into_tables(df,df2,sql.insert_into_tables,cur)
    
