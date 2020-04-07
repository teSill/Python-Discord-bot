from tmdbv3api import TMDb, Movie, TV
import os
import random
import json
from user_data import UserData

tmdb = TMDb()
tmdb.api_key = os.getenv("TMDB_API_KEY")

movie = Movie()
tv = TV()


def get_recommendation(title, minimum_rating):
    try:
        movie_id = movie.search(title)[0].id
    except IndexError:
        movie_id = tv.search(title)[0].id

    pages = []
    amount_of_pages = 10
    for i in range(0, amount_of_pages):
        rnd_num = random.randrange(1, 10)
        pages.append(rnd_num)

    random.shuffle(pages)

    for i in pages:
        try:
            recs = movie.recommendations(movie_id, i)
            random.shuffle(recs)
            for rec in recs:
                if rec.vote_average >= minimum_rating:
                    print(f"Found {rec.title} on page {i}")
                    return rec
        except KeyError:
            continue



class TMDB:
    @classmethod
    def get_popular_movies(cls):
        top_10 = movie.popular()[10:]
        return top_10

    @classmethod
    def get_recommended_movie(cls, username, minimum_rating):
        user = UserData.create_user_instance_by_name(username)

        with open(user.get_full_path_for_edit(), "r+") as f:
            data = json.load(f)
            movies = list(data["Watchlist"][0].keys())
            for i in range(0, len(movies)):
                chosen_movie = random.choice(movies)
                movies.remove(chosen_movie)
                print("Trying to find recommended titles for title: " + str(chosen_movie))
                recommended_movie = get_recommendation(chosen_movie, minimum_rating)
                if recommended_movie is not None:
                    return recommended_movie

            return None


