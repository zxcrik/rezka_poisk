from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name')

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('id', 'poster', 'title_ru', 'title_orig', 'rating', 'prod_year', 'timing', 'premiere_date', 'country_id','genre_id', 'director_id')