from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.authentication import SessionAuthentication
from django.db.models import Q
from .models import *
from .serializers import MovieSerializer, RatingSerializer
import pickle
from ML.ml_model import recommend_movies

class Register(APIView):
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
        
class Logout(APIView):
    permission_classes = (permissions.AllowAny, )
    authentication_classes = ()

    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({'success': 'Logged out successfully'})
        except:
            return Response({'error': 'Failed to Log out'})
        
# view to get all users
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


class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request, format=None):
        return Response({'success': 'CSRF cookie set'})
    

class RateMovies(ListCreateAPIView):
    permission_classes = (permissions.AllowAny, )
    #authentication_classes = (SessionAuthentication,)
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


# gives us the list of movies and the ratings
class MovieView(ListAPIView):
    permission_classes = (permissions.AllowAny, )

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


class MovieRecommendation(APIView):
    permission_classes = (permissions.AllowAny, )

    def recommend_movies(self, request, format=None):
        user_id = request.query_params.get('user_id')
        num_similar_items = 3
        num_of_recs = 3
        recommendation_model = pickle.load(open("ml_model.sav", "rb"))
        
        # Call the recommendation function
        movie_recs = recommendation_model(user_id, num_similar_items, num_of_recs)
        return Response({'recommended_movies': movie_recs})
    
    def get(self, request, format=None):
        return self.recommend_movies(request, format)
