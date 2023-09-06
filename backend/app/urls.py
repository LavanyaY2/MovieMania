from django.urls import path
from .views import *

urlpatterns = [
    path('register', Register.as_view()),
    path('login', Login.as_view()),
    path('logout', Logout.as_view()),
    path('users', GetUsers.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('auth', CheckAuthenticatedView.as_view()),
    path('rate', RateMovies.as_view()),
    path('movies', MovieView.as_view()),
    path('ratings', GetRatings.as_view()),
    path('rec', MovieRecommendation.as_view()),
    
] 
