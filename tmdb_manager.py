from tmdbv3api import TMDb, Movie, TV
import os
import random
import json
from user_data import UserData

tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")

movie = Movie()
tv = TV()


def get_recommendation(title):
    try:
        movie_id = movie.search(title)[0].id
    except IndexError:
        movie_id = tv.search(title)[0].id

    minimum_rating = 6.5

    pages = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(pages)

    for i in pages:
        try:
            recs = movie.recommendations(movie_id, i)
            random.shuffle(recs)
            for rec in recs:
                if rec.vote_average >= minimum_rating:
                    print(rec.title)
                    return rec
        except KeyError as e:
            print("Error retrieving recommendations: " + str(e))




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
            for i in range(0, len(watchlist)):
                chosen_movie = random.choice(list(watchlist.keys()))
                print("Trying to find recommended titles for title: " + str(chosen_movie))
                recommended_movie = get_recommendation(chosen_movie)
                if recommended_movie is not None:
                    print("Returning " + recommended_movie.title)
                    return recommended_movie

            return None


