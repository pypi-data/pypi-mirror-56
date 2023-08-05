import urllib.parse

from django.db import models
from django.urls import reverse


class FilmQuerySet(models.QuerySet):
    def potentially_watchable(self):
        return self.filter(is_watched=False, is_available=True)


class Film(models.Model):
    class Meta:
        unique_together = [["title", "year"]]

    UNIVERSAL = "U"
    PARENTAL_GUIDANCE = "PG"
    AGE_12 = "12"  # Including 12A
    AGE_15 = "15"
    AGE_18 = "18"  # Including R18
    AGE_RATING_CHOICES = [
        (UNIVERSAL, "Universal (4+)"),
        (PARENTAL_GUIDANCE, "Parental Guidance (8+)"),
        (AGE_12, "12+"),
        (AGE_15, "15+"),
        (AGE_18, "18+"),
    ]

    objects = FilmQuerySet.as_manager()

    imdb = models.URLField(verbose_name="IMDB Link")
    title = models.CharField(max_length=255)
    year = models.PositiveIntegerField(verbose_name="Year of Release")
    age_rating = models.CharField(null=True, max_length=3, choices=AGE_RATING_CHOICES)
    imdb_rating = models.FloatField()
    trailer = models.URLField(verbose_name="Trailer Link", null=True, blank=True)
    genre = models.CharField(null=True, blank=True, max_length=255)
    runtime_mins = models.PositiveIntegerField(null=True, blank=True)
    plot = models.TextField(null=True, blank=True)
    poster_url = models.URLField(null=True, blank=True)
    is_available = models.BooleanField(verbose_name="Do we have it?", default=False)
    is_watched = models.BooleanField(verbose_name="Have we watched it?", default=False)

    @property
    def bbfc_search(self):
        url_path = urllib.parse.quote(f"{self.title}")
        return f"https://bbfc.co.uk/search/releases/{url_path}"

    @property
    def youtube_search(self):
        query_string = urllib.parse.urlencode(
            {"search_query": f"{self.title} {self.year} Trailer"}
        )
        return f"https://www.youtube.com/results?{query_string}"

    def get_absolute_url(self):
        return reverse("films:film-update", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.title} ({self.year}) [{self.age_rating}]"

    def __repr__(self):
        return f"<Film(pk={self.pk})>"
