from imdb import IMDb, IMDbError, utils
import urllib

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
        self.image = self.get_gallery()

    def set_instance(self):
        return IMDb()

    def search_movie(self, title):
        return self.instance.search_movie(title)[0]
    
    def get_movie(self, movie_id):
        return self.instance.get_movie(movie_id)
            
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
            
        topActors = 5
        stars = []
        for actor in cast[:topActors]:
            stars.append(actor['name'])
            
        return ", ".join(stars)

    def get_plot(self):
        plot_data = self.imdb_movie.get("plot")
        plot = plot_data[0] if plot_data is not None else "Not found"
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

    def get_url(self):
        return self.instance.get_imdbURL(self.movie)

    def get_gallery(self):
        return self.imdb_movie["cover url"]
            
    
        
