from imdb import IMDb, IMDbError, utils

class IMDbData(object):
    def __init__(self, title):
        self.instance = self.set_instance()
        self.movie = self.search_movie(title)
        self.imdb_movie = self.get_movie(self.movie.getID())
        self.title = self.get_title()
        self.director = self.get_director()
        self.stars = self.get_stars()
        self.plot = self.get_plot()
        self.rating = self.get_rating()
        self.genre = self.get_genres()
        self.year = self.get_year()
        self.runtime = self.get_runtime()
        self.url = self.get_url()

    def set_instance(self):
        try:
            return IMDb()
        except IMDbError as e:
            print("Couldn't initialize the IMDb API: " + e)

    def search_movie(self, title):
        try:
            movie_title = self.instance.search_movie(title)[0]
            return movie_title
        except IMDbError as e:
            print("Couldn't find movie on IMDb: " + e)

    def get_movie(self, movie_id):
        try:
            movie = self.instance.get_movie(movie_id)
            return movie
        except IMDbError as e:
            print("Couldn't get movie from IMDb: " + e)
            
    def get_title(self):
        try:
            title = self.imdb_movie.get("title")
            return title if title is not None else "Not found"
        except IMDbError as e:
            print("Couldn't get movie title from IMDb: " + e)
            
    def get_director(self):
        try:
            director_data = self.imdb_movie.get("director")
            director = director_data[0] if director_data is not None else "Not found"
            return str(director)
        except IMDbError as e:
            print("Couldn't find the movies' directors on IMDb: " + e)

    def get_stars(self):
        try:
            cast = self.imdb_movie.get('cast')
            topActors = 5
            stars = []
            for actor in cast[:topActors]:
                stars.append(actor['name'])
            return ", ".join(stars)
        #todo can shorten this ^ i think
        except IMDbError as e:
            print("Couldn't get the movies' rating from IMDb: " + e)

    def get_plot(self):
        try:
            plot = self.imdb_movie.get("plot")[0]
            return plot
        except IMDbError as e:
            print("Couldn't find the movies' plot on IMDb: " + e)
            
    def get_rating(self):
        try:
            return str("%s/10" % self.imdb_movie.get("rating"))
        except IMDbError as e:
            print("Couldn't get the movies' rating from IMDb: " + e)
            
    def get_genres(self):
        try:
            return ", ".join(self.imdb_movie.get("genre"))
        except IMDbError as e:
            print("Couldn't get the movies' genres from IMDb: " + e)

    def get_year(self):
        try:
            return self.imdb_movie.get("year")
        except IMDbError as e:
            print("Couldn't get the movies' release date from IMDb: " + e)

    def get_runtime(self):
        try:
            return str(self.imdb_movie.get("runtime")[0]) + "min"
        except IMDbError as e:
            print("Couldn't get the movies' runtime from IMDb: " + e)

    def get_url(self):
        try:
            return self.instance.get_imdbURL(self.movie)
        except IMDbError as e:
            print("Couldn't get the movies' URL from IMDb: " + e)
            
    def is_series(self):
        self.instance.update(self.movie, "episodes")
        return len(self.movie["episodes"]) > 1
        
