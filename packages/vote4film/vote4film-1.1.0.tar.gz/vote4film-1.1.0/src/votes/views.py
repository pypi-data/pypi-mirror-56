from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from films.models import Film
from votes.forms import VoteForm
from votes.logic import next_film_to_vote
from votes.models import Vote


class NoMoreFilms(Exception):
    pass


class VoteCreate(CreateView):
    model = Vote
    form_class = VoteForm

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except NoMoreFilms:
            messages.success(request, "There are no new films to vote for.")
            return redirect("web:home")

    def get_initial(self):
        # Set the film that we are voting for
        initial = super().get_initial()
        film = next_film_to_vote(self.request.user)
        if not film:
            raise NoMoreFilms("No more films to vote for")

        initial["film"] = film
        initial["user"] = self.request.user.pk
        return initial

    def get_form_kwargs(self):
        # Ensure form always has the current user present
        kwargs = super().get_form_kwargs()
        # Only have data when posting
        if "data" in kwargs:
            data = kwargs["data"].copy()
            data["user"] = self.request.user.pk
            kwargs["data"] = data

        return kwargs

    def get_context_data(self, **kwargs):
        # Provide easier access to film in the template
        context = super().get_context_data(**kwargs)
        context["film"] = context["form"].initial["film"]
        return context

    def form_valid(self, form):
        # Set the form's user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Continue reviewing if and only if there are cards to review
        if next_film_to_vote(self.request.user):
            return reverse("votes:vote-create")
        else:
            messages.success(self.request, "You have voted for all of the films.")
            return reverse("web:home")


class VoteAggregate(ListView):
    model = Film
    template_name = "votes/vote_aggregate.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(score=Sum("vote__choice"))
            .order_by("is_watched", "-score", "id")
            .prefetch_related("vote_set", "vote_set__user")
        )
