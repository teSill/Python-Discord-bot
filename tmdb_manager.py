from tmdbv3api import TMDb, Movie as tmdb_movie
import os

tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")
tmdb_m = tmdb_movie()

class TMDB:
    def get_popular_movies():
        top_10 = tmdb_m.popular()[10:]
        return top_10
        
