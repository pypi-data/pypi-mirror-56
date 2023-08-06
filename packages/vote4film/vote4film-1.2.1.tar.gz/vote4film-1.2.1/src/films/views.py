from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
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

        try:
            return super().form_valid(form)
        except IntegrityError as err:
            if err.args[0] == Film.DUPLICATE_ERROR_TEXT:
                self.object = Film.objects.get(title=film.title, year=film.year)
                return HttpResponseRedirect(self.get_success_url())

            raise

    def get_success_url(self):
        if "_save" in self.request.POST:
            return reverse("votes:vote-create")
        elif "_edit" in self.request.POST:
            return super().get_success_url()
        elif "_addanother" in self.request.POST:
            return reverse("films:film-create")


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
