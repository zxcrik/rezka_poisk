from rest_framework import serializers
from .models import *

class Film(serializers.Serializer):
    poster = serializers.ImageField(source='poster.url')
    title_ru = serializers.CharField(max_length=255)
    title_orig  = serializers.CharField(max_length=255)
    rating = serializers.FloatField(max_value=10)
    prod_year = serializers.IntegerField(min_value=1900 ,max_value=2030)
    timing = serializers.IntegerField(max_length=None)
    premiere_date = serializers.DateField(blank=True)
    country_id = serializers.ForeignKey(Country, on_delete=models.CASCADE)
    genre_id = serializers.ForeignKey(Genre, on_delete=models.CASCADE)
    director_id = serializers.ForeignKey(Director,on_delete=models.CASCADE)

    def __str__(self):
        return self.title_orig