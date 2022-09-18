from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

#API AUTH

class UserSerializer(serializers.ModelSerializer):
     class Meta:
         model = User
         fields = '__all__'
#API AUTH


class ListeMaison(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

class composition(serializers.ModelSerializer):
    class Meta:
        model = Composition
        fields = '__all__'

class infrastructure(serializers.ModelSerializer):
    class Meta:
        model = Infrastructure
        fields = '__all__'

class Catego(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class maison(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'
