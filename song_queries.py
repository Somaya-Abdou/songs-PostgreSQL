import song_create_tables as song

def main():
   
#getting average of popularity for each song in each country
    avg_popularity = song.cur.execute("""with t1 as(
                                           select g.name,c.country,r.popularity
                                           from general_table g 
                                           join rating_table r on r.spotify_id = g.spotify_id
                                           join country_table c on c.code = g.country
                                           order by 2)

                                select t1.name,t1.country,avg(t1.popularity) as avg_popularity
                                from t1
                                group by 1,2
                                order by 3 desc
                              """)
    result = song.cur.fetchall()
    columns = [desc[0] for desc in song.cur.description]
    for row in result:
        print (dict(zip(columns, row)))                          
    print("\n")  
    print("\n")  

#getting descriptions of most popular songs worlwide
    avg_song_description_of_most_popular_worldwide = song.cur.execute("""with t1 as(
                                select g.name,c.country,r.popularity,g.spotify_id
                                from general_table g 
                                join rating_table r on r.spotify_id = g.spotify_id
                                join country_table c on c.code = g.country
                                order by 2),

                                                            t3 as(
                                select t2.name,t2.country,t2.avg_popularity,
                                       t2.avg_popularity_ntile,t2.spotify_id
                                from(
                                       select t1.name,t1.country,t1.spotify_id,
                                               avg(t1.popularity) as avg_popularity,
                                               ntile(10) over( order by avg(t1.popularity) desc ) as avg_popularity_ntile
                                       from t1
                                       group by 1,2,3
                                       order by 3 desc)t2
                                 where avg_popularity_ntile = 1)

                          select avg(s.danceability) as avg_dance,avg(s.energy)as avg_energy,
                                 avg(s.loudness)as avg_loudness,avg(s.speechiness)as avg_speech,
	                              avg(s.acousticness)as avg_acoustic,avg(s.instrumentalness)as avg_instrument
                          from t3 
                          join song_description_table as s 
                          on t3.spotify_id = s.spotify_id
                                                     """)
    result = song.cur.fetchall()
    columns = [desc[0] for desc in song.cur.description]
    for row in result:
        print (dict(zip(columns, row)))                          
    print("\n")  
    print("\n")  

#getting most popular song in each country
    most_popular_songs = song.cur.execute("""
       with t1 as(
          select g.name,c.country,r.popularity
          from general_table g 
          join rating_table r on r.spotify_id = g.spotify_id
          join country_table c on c.code = g.country
          order by 2)

       select t2.country,t2.most_popular_song,max(t2.most_popular_value)as value_of_popularity
       from(
          select t1.country,t1.name,t1.popularity,
	            first_value(t1.popularity) over(partition by t1.country order by t1.popularity desc) as most_popular_value,
	            first_value(t1.name) over(partition by t1.country order by t1.popularity desc) as most_popular_song
          from t1
          group by 1,2,3)t2
       group by 1,2
       order by 3 desc
                                 """)
    result = song.cur.fetchall()
    columns = [desc[0] for desc in song.cur.description]
    for row in result:
        print (dict(zip(columns, row)))                          
    print("\n")
    print("\n")    

#getting average desired value of danceability,acousticness, etc for each country
    avg_desired_specs_of_songs = song.cur.execute("""select c.country,avg(s.danceability)avg_dance,avg(s.energy)as avg_energy,
                                                   avg(s.loudness)as avg_loudness,avg(s.speechiness)as avg_speech,
	                                                avg(s.acousticness)as avg_acoustic,
                                                   avg(s.instrumentalness)as avg_instrument
                                            from general_table as g
                                            join country_table as c on c.code = g.country
                                            join rating_table as r on r.spotify_id = g.spotify_id
                                            join song_description_table as s on s.spotify_id = g.spotify_id
                                            group by 1
                                            order by 1 
                                          """)
 
    result = song.cur.fetchall()
    columns = [desc[0] for desc in song.cur.description]
    for row in result:
        print (dict(zip(columns, row)))                          
    print("\n") 
    print("\n")   
  
#getting best and average ranking song in each country 
    best_song_each_country = song.cur.execute("""select g.name,c.country, r.daily_rank,
cast(avg(r.daily_rank) over (partition by c.country order by (select Null))as decimal(4,2)) as avg_ranking_in_country,
cast(min(avg(r.daily_rank)) over (partition by c.country order by (select Null))as decimal(4,2)) as best_ranking_song_in_country
                                            from general_table as g
                                            join rating_table as r on r.spotify_id = g.spotify_id
                                            join country_table as c on c.code = g.country
                                            group by 2,1,3
                                            order by 2      
                                          """) 
    result = song.cur.fetchall()
    columns = [desc[0] for desc in song.cur.description]
    for row in result:
        print (dict(zip(columns, row)))                          
    print("\n")
    print("\n")                                        

#getting best and average ranking of each song
    best_ranking_each_song = song.cur.execute("""select g.name,c.country, r.daily_rank,
cast(avg(r.daily_rank) over (partition by g.name order by (select Null))as decimal(4,2)) as avg_ranking_of_song,
cast(min(avg(r.daily_rank)) over (partition by g.name order by (select Null))as decimal(4,2)) as best_ranking_song
                                            from general_table as g
                                            join rating_table as r on r.spotify_id = g.spotify_id
                                            join country_table as c on c.code = g.country
                                            group by 1,2,3
                                            order by 1
                                          """)    
    result = song.cur.fetchall()
    columns = [desc[0] for desc in song.cur.description]
    for row in result:
        print (dict(zip(columns, row)))                          
    print("\n")  
    print("\n")                                                                              
     

main()      
