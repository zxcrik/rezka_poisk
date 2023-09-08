from django.db import models
import uuid

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

class Film(models.Model):
    poster = models.ImageField(blank=True, upload_to=uniq_name_upload)
    title_ru = models.CharField(max_length=255)
    title_orig  = models.CharField(max_length=255)
    rating = models.FloatField(max_length=10)
    prod_year = models.IntegerField(max_length=2030)
    timing = models.IntegerField(max_length=None)
    premiere_date = models.DateField(blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    director = models.ForeignKey(Director,on_delete=models.CASCADE)

    def __str__(self):
        return self.title_orig
