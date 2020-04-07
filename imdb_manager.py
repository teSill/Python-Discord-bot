from imdb import IMDb, IMDbError, utils
import urllib
from utils import Utility
import random
import re

instance = IMDb()


def search_movie(title):
    return instance.search_movie(title)[0]


def get_movie(movie_id):
    return instance.get_movie(movie_id)


def get_movie_url(title):
    movie = instance.search_movie(title)[0]
    return instance.get_imdbURL(movie)


class IMDbMovieData:
    def __init__(self, title):
        self.movie = search_movie(title)
        self.imdb_movie = get_movie(self.movie.getID())
        self.title = self.get_title()
        self.director = self.get_director()
        self.stars = self.get_stars()
        self.plot = self.get_plot()
        self.rating = self.get_rating()
        self.genre = self.get_genres()
        self.year = self.get_year()
        self.runtime = self.get_runtime()
        self.url = get_movie_url(title)
        self.image = self.get_gallery()

    def get_title(self):
        return self.imdb_movie.get("title")

    def get_director(self):
        director_data = self.imdb_movie.get("director")
        director = director_data[0] if director_data is not None else "Not found"
        return str(director)

    def get_stars(self):
        cast = self.imdb_movie.get('cast')

        if cast is None:
            return "Not found"

        top_actors = 5
        stars = []
        for actor in cast[:top_actors]:
            stars.append(actor['name'])

        return ", ".join(stars)

    def get_plot(self):
        plot_data = self.imdb_movie.get("plot")
        plot = plot_data[0] if plot_data is not None else "Not found"
        if "::" in plot:
            plot = plot.split("::")[0]
        return plot

    def get_rating(self):
        return str("%s/10" % self.imdb_movie.get("rating"))

    def get_genres(self):
        return ", ".join(self.imdb_movie.get("genre"))

    def get_year(self):
        return self.imdb_movie.get("year")

    def get_runtime(self):
        runtime_data = self.imdb_movie.get("runtime")
        runtime = str(runtime_data[0]) + "min" if runtime_data is not None else "Not found"
        return runtime

    def get_gallery(self):
        return self.imdb_movie["cover url"]

    @classmethod
    def get_cover_image_url(cls, title):
        movie = search_movie(title)
        imdb_movie = get_movie(movie.getID())
        return imdb_movie["cover url"]


def search_actor_name(name):
    return instance.search_person(name)[0]


class IMDbActorData:
    def __init__(self, name):
        self.actor_obj = search_actor_name(name)
        self.id = self.actor_obj.personID
        # self.person_obj = instance.get_person(self.actor_obj.personID)
        # self.filmography = self.get_filmography()
        self.biography = self.get_biography()
        self.thumbnail = self.get_thumbnail()
        self.cover = self.get_full_size_image()
        # self.awards = self.get_awards()
        self.url = self.get_url()

    def get_filmography(self):
        person = instance.get_person(self.id)
        movies = []

        for index, movie in enumerate(person['filmography']["actor"]):
            if index == 5:
                break

            movies.append(movie["title"])
        return movies

    def get_biography(self):
        person = instance.get_person(self.id)
        if person is None:
            return "Not found"

        split_bio = str(person["bio"]).split(".")
        split_bio = [item + "." for item in split_bio]

        mini_bio = split_bio[:5]
        mini_bio[2] = mini_bio[2] + "\n\n"
        mini_bio_str = "".join(mini_bio)
        return mini_bio_str[2:]

    def get_thumbnail(self):
        person = instance.get_person(self.id)
        return person["headshot"]

    def get_full_size_image(self):
        person = instance.get_person(self.id)
        return person["full-size headshot"]

    def get_awards(self):
        pass

    def get_url(self):
        return instance.get_imdbURL(self.actor_obj)
