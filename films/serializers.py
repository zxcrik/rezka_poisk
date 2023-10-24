from rest_framework import serializers
from .models import *

# class FilmSerializer(serializers.Serializer):
    # poster = serializers.ImageField(use_url='poster.url')
    # title_ru = serializers.CharField(max_length=255)
    # title_orig  = serializers.CharField(max_length=255)
    # prod_year = models.IntegerField()
    # timing = models.IntegerField()
    # premiere_date = models.DateField()
    # country_id = serializers.IntegerField()
    # genre_id = serializers.IntegerField()
    # director_id = serializers.IntegerField()

    # def create(self, vailidated_data):
    #     return Film.objects.create(**vailidated_data)
    
    # def update(self, instance, vailidated_data):
    #     instance.poster = vailidated_data.get('poster', instance.poster)    # Оставить оригинальный как defalt #
    #     instance.title_ru  = vailidated_data.get('title_ru', instance.title_ru) 
    #     instance.title_orig = vailidated_data.get('title_orig', instance.title_orig) 
    #     instance.prod_year  = vailidated_data.get('prod_year', instance.prod_year) 
    #     instance.timing = vailidated_data.get('timing', instance.timing) 
    #     instance.premiere_date = vailidated_data.get('premiere_date', instance.premiere_date) 
    #     instance.country_id = vailidated_data.get('country_id', instance.country_id) 
    #     instance.genre_id = vailidated_data.get('genre_id', instance.genre_id) 
    #     instance.director_id = vailidated_data.get('director_id', instance.director_id) 

    #     instance.save()
    #     return instance
    

class FilmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'