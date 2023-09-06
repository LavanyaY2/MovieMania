# data processing
import pandas as pd
import numpy as np

# data visualization
import seaborn as sns
import matplotlib.pyplot as plt

# for metrics
from sklearn import metrics
import scipy.stats
import operator
import pickle

# for item similarity
from sklearn.metrics.pairwise import cosine_similarity

# getting the csv data
# movies = pd.read_csv('./movies.csv')
# ratings = pd.read_csv('./rating.csv')

from app.models import *

movie = Movie.objects.values() 
rating = Rating.objects.values() 

# PREPROCESSING STEPS

# converting querysets to dataframes
movies = pd.DataFrame(movie)
ratings = pd.DataFrame(rating)

print("RATINGS")
print(ratings)


# check for missing data
# ratings.isnull().sum()
# movies.isnull().sum()

# combining the two dataframes using the movieId as the key
df = pd.merge(movies, ratings, left_on='id', right_on='movie_id', how='inner')
grouped_by_movie = df.groupby('title')
grouped_by_movie = grouped_by_movie.agg(num_of_ratings = ('rating', 'count'), mean_rating = ('rating', 'mean'))
grouped_by_movie = grouped_by_movie.reset_index()

print("get 50 movies")
print(grouped_by_movie)

# to make sure that we are not overestimating, we will remove all the movies
# with less than 50 ratings
# movies_gt50 = grouped_by_movie[grouped_by_movie['num_of_ratings'] > 1]


# so we inner join the movies_gt50 df with the original df that has all the movies 
# to get just movies with more than 50 ratings in our actual dataset
df_gt50 = pd.merge(df, grouped_by_movie[['title']], on='title', how='inner')

print("get 50 movies")
print(df_gt50)

# now we have the number of movies that have more than 50 ratings
# we now transform the df into a user-item interaction matrix
user_item_matrix = df_gt50.pivot_table(index='title', columns='user_id', values='rating')

print("user item matrix")
print(user_item_matrix)

# now we normalize the data to remove bias
# in this case, we use the min-max normalization technique to scale the data
# between 0 and 1
def normalize_data(row):
    normalized_row = (row - row.mean())/(row.max() - row.min())
    return normalized_row
    
normalized_user_item_matrix = user_item_matrix.apply(normalize_data)

print("MATRIX")
print(normalized_user_item_matrix.fillna(0))

# calculating similarity - using cosine similarity
item_similarity = cosine_similarity(normalized_user_item_matrix.fillna(0))
item_similarity_df = pd.DataFrame(item_similarity, index=normalized_user_item_matrix.T.columns, columns=normalized_user_item_matrix.T.columns)

def recommend_movies(user_id, num_similar_items, num_of_recs):

    # to find the unwatched movies, we need to take the list of all movies 
    # that have ratings,
    # and then we check if the user has rated that movie
    # if the user hasnt rated, we put it in the unwatched list
    # and then 

    print("checks")
    print(user_item_matrix.columns)
    print(user_id)

    if int(user_id) in user_item_matrix.columns:

        print("BITCH")
        print(user_id)

        total_movies_for_user = normalized_user_item_matrix[int(user_id)]


        #new code
        total_movies_for_user = total_movies_for_user.fillna(0) 

        unwatched_movies = pd.DataFrame(total_movies_for_user.eq(0))

    

        unwatched_movies = unwatched_movies.reset_index()
        unwatched_movies = unwatched_movies[unwatched_movies[int(user_id)] == True]['title'].values.tolist()
        
        print("UNWATCHED MOVIES")
        print(unwatched_movies)

        
        watched_movies = pd.DataFrame(normalized_user_item_matrix[int(user_id)].dropna(axis=0, how='all'))
        watched_movies = watched_movies.rename(columns={int(user_id): 'rating'})

        print("WATCHED MOVIES")
        print(watched_movies)

        # now we predict the user ratings for the unwatched movies
        predict_rating = {}

        for movie in unwatched_movies:
            # calculate similarity score of target movie with other movies
            # we can use the KNN model here to find the neighbor movies of the 
            # target movie here 

            target_movie_similarity_score = item_similarity_df[[movie]].rename(columns={movie: 'similarity score with target movie'})

            print("TARGET MOVIE SIM SCORE")
            print(target_movie_similarity_score)

            # and now to predict the ratings for the unwatched movies
            # we first find the similarity with the watched movies
            target_movie_watched_similarity = watched_movies.merge(target_movie_similarity_score, on='title', how='inner').sort_values('similarity score with target movie', ascending=True)
            
            print("TARGET MOVIE SIM SCORE WITH WATCHED")
            print(target_movie_similarity_score)
            
            target_movie_watched_similarity = target_movie_watched_similarity[:num_similar_items]

            # # finding 0 indices
            # zero_sim = target_movie_watched_similarity['similarity score with target movie'] == 0
            # zero_indices = target_movie_watched_similarity[zero_sim].index

            # print("0 indices")
            # print(zero_indices)

            # for indices in zero_indices:
            #     predicted_rating = np.average(target_movie_watched_similarity['rating'])


            # print("WEIGHT")
            # print(target_movie_watched_similarity)
            # print("TARGET MOVIE WATCHED SIMILARITY RATING")
            # print(target_movie_watched_similarity['rating'])

            # if weight = 0, that means no similarity so we just use the average
            # of the ratings of the user to predict potential rating
            
            # sim = target_movie_watched_similarity['similarity score with target movie'] != 0
            # sim_list = target_movie_watched_similarity[sim].index

            # print("sim list")
            # print(sim_list)

            # for index in sim_list:
            #     predicted_rating = np.average(target_movie_watched_similarity['rating'], weights=target_movie_watched_similarity['similarity score with target movie'])
            
            # now we calculate the predicted rating
            
            # checking if sum of weights is 0
            sum_weights = target_movie_watched_similarity['similarity score with target movie'].sum()

            if sum_weights == 0 :
                print("TEST")
                print(target_movie_watched_similarity['rating'])
                predicted_rating = np.average(target_movie_watched_similarity['rating'])
                print("PREDICTED RATING")
                print(predicted_rating)
                predicted_rating = round(predicted_rating, 6)
            else:
                print("TEST 2 ")
                predicted_rating = np.average(target_movie_watched_similarity['rating'], weights=target_movie_watched_similarity['similarity score with target movie'])
            
            print("PREDICTED RATING FOR THE MOVIE")
            print(predicted_rating)

            predicted_rating = round(predicted_rating, 6)
            predict_rating[movie] = predicted_rating
            recommended_movies = dict(sorted(predict_rating.items(), key= lambda item: item[1], reverse=True)[:num_of_recs])
    else:
        recommended_movies = None

    return recommended_movies

# now to pickle, we pickle the recommend_movies algorithm only
pickle.dump(recommend_movies, open("ml_model.sav", "wb"))