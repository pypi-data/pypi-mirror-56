from django.views.generic.base import TemplateView

from schedule.logic import get_schedule


class Schedule(TemplateView):
    template_name = "schedule/schedule.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        (
            kwargs["event"],
            kwargs["film"],
            kwargs["present_users"],
            kwargs["absent_users"],
            kwargs["unknown_users"],
        ) = get_schedule()
        return kwargs
