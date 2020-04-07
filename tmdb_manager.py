from tmdbv3api import TMDb, Movie
import os
import random
import json
from user_data import UserData

tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")
movie = Movie()


class TMDB:
    @classmethod
    def get_popular_movies(cls):
        top_10 = movie.popular()[10:]
        return top_10

    @classmethod
    def get_recommended_movie(cls, username):
        user = UserData.create_user_instance_by_name(username)

        with open(user.get_full_path_for_edit(), "r+") as f:
            data = json.load(f)
            watchlist = data["Watchlist"][0]
            print(watchlist)
            chosen_movie = random.choice(list(watchlist.keys()))

        print("getting recommendation based on title: " + chosen_movie)
        movie_id = movie.search(chosen_movie)[0].id

        recommendations = movie.recommendations(movie_id)
        recommended_movie = random.choice(recommendations)
        return recommended_movie


