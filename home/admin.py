from django.contrib import admin
from .models import Film,Comment, RateFilm

# Register your models here.
admin.site.register(Film)

admin.site.register(Comment)

admin.site.register(RateFilm)
