from django.db import models
from django.contrib.auth.models import User

# we use the default django User model for user info

# model for the Movies - stores only the movies from the dataset
class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=500)

    def __str__(self):
        return self.title
    
# the rating model will store the ratings associated with each user id and movie id
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None)
    rating = models.FloatField()

    def __str__(self):
        return self.rating