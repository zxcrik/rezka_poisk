from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import datetime
import uuid
import os 

# Create your models here.
def uniq_name_upload(instance, filename):
    new_file_name = f"{uuid.uuid4()}.{filename.split('.')[-1]}"
    return f'images/{new_file_name}'


class Country(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Director(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Grade(models.Model):
    film_grade = models.FloatField(max_length=10.0)

    class Meta:
        verbose_name = 'film_grade'
        verbose_name_plural = 'films_grade'

    def __float__(self):
        return self.film_grade

class Film(models.Model):
    poster = models.ImageField(blank=True, upload_to=uniq_name_upload)
    title_ru = models.CharField(max_length=255)
    title_orig  = models.CharField(max_length=255)
    prod_year = models.IntegerField()
    timing = models.IntegerField()
    premiere_date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    director = models.ForeignKey(Director,on_delete=models.CASCADE)
    rating = models.ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return self.title_orig

    def delete(self, *args, **kwargs):
        if self.poster and os.path.isfile(self.poster.path):
            os.remove(self.poster.path)

        super().delete(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=2000)
    date = models.DateTimeField(default=datetime.datetime.today())
    film = models.ForeignKey(Film, on_delete=models.CASCADE, default=1)

class LikedFilm(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked film: {self.film.title_orig}"
