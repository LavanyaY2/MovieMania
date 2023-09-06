from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import CreateAPIView
from rest_framework import permissions, status
from django.contrib import auth
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from .serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication

from django.db.models import Q
from rest_framework.decorators import api_view

# for recommendation model
from .models import *
from .serializers import MovieSerializer, RatingSerializer, MovieRecSerializer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# for item similarity
from sklearn.metrics.pairwise import cosine_similarity
import operator


# the sign up view - csrf protected 
#@method_decorator(csrf_protect, name='dispatch')
class Register(APIView):
    # set permission classes to allow any - doesn't need to have csrf protection
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data
        username = data['username']
        password = data['password']
        re_password = data['re_password']

        if password == re_password:
            # checking if user account exists
            if User.objects.filter(username=username).exists():
                return Response({'error': 'User account already exists'})
            else:
                if len(password) < 6:
                    return Response({'error': 'Password too short'})
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()
                    return Response({'success': 'User created successfully'})
        else:
            return Response({'error': 'Passwords do not match'})

#@method_decorator(ensure_csrf_cookie, name='dispatch')
class Login(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = (SessionAuthentication,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            auth.login(request, user)
            return Response({'success': 'Logged in', 'username': username})
        else:
            return Response({'error': 'Failed to Log in'})
        
# because we are already authenticated, we are already csrf protected here
class Logout(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()

    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'Logged out successfully'})
        except:
            return Response({'error': 'Failed to Log out'})
        
# view to get users
class GetUsers(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format = None):
        users = User.objects.all()
        users = UserSerializer(users, many=True)
        return Response(users.data)
    
# check if user is authenticated
class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        try:
            isAuthenticated = User.is_authenticated
            if isAuthenticated:
                return Response({'isAuthenticated': 'success'})
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'something went wrong'})


# we need to get the csrf token in our react application
#@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
    


# the listcreateapi view helps us create get and post methods
class RateMovies(ListCreateAPIView):
    permission_classes = (permissions.AllowAny, )
    #authentication_classes = (SessionAuthentication,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


# gives us the list of movies and the ratings
class MovieView(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    #queryset = Movie.objects.all()

    serializer_class = MovieSerializer
    def get_queryset(self):
        limit = self.request.GET.get('limit')  # Get the limit from the query parameter
        queryset = Movie.objects.all()
        if limit:
            queryset = queryset[:int(limit)]  # Limit the queryset based on the limit

        return queryset

# to get the ratings
class GetRatings(ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


import pickle
from ML.ml_model import recommend_movies


class MovieRecommendation(APIView):
    permission_classes = (permissions.AllowAny, )

    def recommend_movies(self, request, format=None):
        print(request.query_params)
        user_id = request.query_params.get('user_id')
        num_similar_items = 3
        num_of_recs = 3

        print("TEST")
        print(user_id)

        recommendation_model = pickle.load(open("ml_model.sav", "rb"))
        
        print("LOADED MODEL")

        # Call the recommendation function
        movie_recs = recommendation_model(user_id, num_similar_items, num_of_recs)

        print("recommended movies")
        print(movie_recs)
        return Response({'recommended_movies': movie_recs})
    
    def get(self, request, format=None):
        return self.recommend_movies(request, format)

# class MovieRecommendation(APIView):
#     permission_classes = (permissions.AllowAny, )
#     def get(self, request, format=None):
#         user_id = request.user.id
#         num_similar_items = 3
#         num_of_recs = 3

#         print("TEST")
#         print(request.user.id)

#         recommendation_model = pickle.load(open("ml_model.sav", "rb"))
        
#         print("LOADED MODEL")

#         # Load the pickled recommendation model
#         # with open('ml_model.sav', 'rb') as model_file:
#         #     recommendation_model = pickle.load(model_file)

#         # Call the recommendation function
#         movie_recs = recommendation_model(user_id, num_similar_items, num_of_recs)

#         print("recommended movies")
#         print(movie_recs)
#         return Response({'recommended_movies': movie_recs})