from django.contrib import admin

from votes import models

admin.site.register(models.Vote)
