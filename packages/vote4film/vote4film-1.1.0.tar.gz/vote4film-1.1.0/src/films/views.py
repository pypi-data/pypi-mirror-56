from django.conf import settings
from django.views.generic.edit import CreateView, UpdateView

from films.clients import omdb
from films.models import Film


class FilmCreate(CreateView):
    model = Film
    fields = ["imdb", "is_available"]

    def form_valid(self, form):
        self.object = form.save(commit=False)
        film = omdb.get_film(settings.OMDB_API_KEY, self.object.imdb)
        self.object.title = film.title
        self.object.year = film.year
        self.object.age_rating = film.age_rating.value if film.age_rating else None
        self.object.imdb_rating = film.imdb_rating
        self.object.genre = film.genre
        self.object.runtime_mins = film.runtime_mins
        self.object.plot = film.plot
        self.object.poster_url = film.poster_url
        return super().form_valid(form)


class FilmUpdate(UpdateView):
    model = Film
    fields = [
        "imdb",
        "year",
        "age_rating",
        "imdb_rating",
        "genre",
        "runtime_mins",
        "plot",
        "poster_url",
        "trailer",
        "is_available",
        "is_watched",
    ]
