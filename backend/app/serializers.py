from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

# now we can get the ratings of each user
class UserSerializer(serializers.ModelSerializer):

    ratings = RatingSerializer(read_only=True, many=True, source="rating_set")
    class Meta:
        model = User
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


