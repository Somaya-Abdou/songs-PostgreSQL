drop_database = """Drop database if exists songs"""
create_database = """Create database songs """

drop_general_table= """Drop table if exists public.general_table"""
drop_rating_table = """Drop table if exists public.rating_table"""
drop_time_table = """Drop table if exists public.time_table"""
drop_song_description_table = """Drop table if exists public.song_description_table"""
drop_country_table = """Drop table if exists public.country_table"""

create_general_table = """Create table if not exists public.general_table(
                                 spotify_id varchar Primary key,
                                 name varchar not null,
                                 artists varchar ,
                                 album_name varchar ,
                                 country varchar,
                                 is_explicit bool 
                                                                         )"""

create_rating_table = """Create table if not exists public.rating_table(
                                general_id int  Primary Key,
                                spotify_id varchar,
                                daily_rank int ,
                                daily_movement int ,
                                weekly_movement int ,
                                popularity int 
                                                                       )"""

create_time_table = """Create table if not exists public.time_table(
                              spotify_id varchar Primary Key,
                              duration_min float ,
                              album_release_day int ,
                              album_release_month int ,
                              album_release_year int ,
                              time_signature int
                                                                   )"""  

create_song_description_table = """Create table if not exists public.song_description_table(
                                         spotify_id varchar Primary key,
                                         danceability float ,
                                         energy float ,
                                         loudness float ,
                                         speechiness float ,
                                         acousticness float ,
                                         instrumentalness float ,
                                         liveness float                                         
                                                                                          )"""
create_country_table = """Create table if not exists public.country_table(
                                 country  varchar Primary Key,
                                 code  varchar
                                                                          )"""

insert_into_general_table = """Insert into general_table (spotify_id ,name ,artists,
                                                          album_name ,country,is_explicit)
                                values(%s,%s,%s,%s,%s,%s) 
                                ON CONFLICT (spotify_id) DO NOTHING
                            """
insert_into_rating_table = """Insert into rating_table (general_id,spotify_id ,daily_rank ,daily_movement ,
                                                        weekly_movement ,popularity )
                               values(%s,%s,%s,%s,%s,%s)
                           """
insert_into_time_table = """Insert into time_table (spotify_id ,duration_min ,album_release_day ,
                                                    album_release_month ,album_release_year ,time_signature)
                             values(%s,%s,%s,%s,%s,%s) 
                             ON CONFLICT (spotify_id) DO NOTHING
                         """
insert_into_song_description_table = """Insert into song_description_table (spotify_id ,danceability ,energy ,
                                                                           loudness ,speechiness ,acousticness ,
                                                                           instrumentalness ,liveness)
                                       values(%s,%s,%s,%s,%s,%s,%s,%s)
                                       ON CONFLICT (spotify_id) DO NOTHING
                                    """
insert_into_country_table = """Insert into country_table (country ,code)
                               values(%s,%s)
                            """

drop_tables = [drop_general_table,drop_rating_table,drop_time_table,\
               drop_song_description_table ,drop_country_table]
create_tables = [create_general_table,create_rating_table,create_time_table,\
                 create_song_description_table,create_country_table]
insert_into_tables = [insert_into_general_table ,insert_into_rating_table ,\
                      insert_into_time_table ,insert_into_song_description_table ,insert_into_country_table]