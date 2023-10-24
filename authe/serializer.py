from rest_framework import serializers
from .models import User


class UserRetrieveSerializer(serializers.ModelSerializer):   # Получаеь данные user-a #
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name','image', 'email')
        
class UserCreateSerializer(serializers.ModelSerializer):     # Создание user-a #
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name','password', 'email', 'image')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user