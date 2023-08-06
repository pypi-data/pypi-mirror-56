from django.urls import reverse

from calender.models import Register


def next_event_register_url(request):
    if not request.user.is_authenticated:
        return {}

    register = Register.objects.next_event_register(request.user)
    if not register:
        return {}

    return {
        "next_event_register_url": reverse(
            "calender:register-update", args=(register.pk,)
        )
    }
