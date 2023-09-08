# for data processing
import pandas as pd
import numpy as np

# for metrics
from sklearn import metrics
import scipy.stats
import operator
import pickle

# for item similarity
from sklearn.metrics.pairwise import cosine_similarity

from app.models import *

movie = Movie.objects.values() 
rating = Rating.objects.values() 

# PREPROCESSING STEPS

# convert querysets to dataframes
movies = pd.DataFrame(movie)
ratings = pd.DataFrame(rating)

# combine the two dataframes using the movieId as the key
df = pd.merge(movies, ratings, left_on='id', right_on='movie_id', how='inner')
grouped_by_movie = df.groupby('title')
grouped_by_movie = grouped_by_movie.agg(num_of_ratings = ('rating', 'count'), mean_rating = ('rating', 'mean'))
grouped_by_movie = grouped_by_movie.reset_index()
df_gt50 = pd.merge(df, grouped_by_movie[['title']], on='title', how='inner')

# transform the df into a user-item interaction matrix
user_item_matrix = df_gt50.pivot_table(index='title', columns='user_id', values='rating')

# normalize the data to remove bias
# in this case, the min-max normalization technique is used to scale the data between 0 and 1
def normalize_data(row):
    normalized_row = (row - row.mean())/(row.max() - row.min())
    return normalized_row
    
normalized_user_item_matrix = user_item_matrix.apply(normalize_data)

# calculating similarity - using cosine similarity
item_similarity = cosine_similarity(normalized_user_item_matrix.fillna(0))
item_similarity_df = pd.DataFrame(item_similarity, index=normalized_user_item_matrix.T.columns, columns=normalized_user_item_matrix.T.columns)

# MOVIE RECOMMENDATION ALGORITHM
def recommend_movies(user_id, num_similar_items, num_of_recs):

    # to find the unwatched movies, take the list of all movies that have ratings,
    # and then check if the user has rated that movie. If the user hasn't rated, 
    # put it in the unwatched list

    if int(user_id) in user_item_matrix.columns:
        total_movies_for_user = normalized_user_item_matrix[int(user_id)]
        total_movies_for_user = total_movies_for_user.fillna(0) 
        unwatched_movies = pd.DataFrame(total_movies_for_user.eq(0))
        unwatched_movies = unwatched_movies.reset_index()
        unwatched_movies = unwatched_movies[unwatched_movies[int(user_id)] == True]['title'].values.tolist()
        watched_movies = pd.DataFrame(normalized_user_item_matrix[int(user_id)].dropna(axis=0, how='all'))
        watched_movies = watched_movies.rename(columns={int(user_id): 'rating'})

        # predict the user ratings for the unwatched movies
        predict_rating = {}

        for movie in unwatched_movies:
            # calculate similarity score of target movie with other movies
            target_movie_similarity_score = item_similarity_df[[movie]].rename(columns={movie: 'similarity score with target movie'})

            # to predict the ratings for the unwatched movies, find the similarity with the watched movies
            target_movie_watched_similarity = watched_movies.merge(target_movie_similarity_score, on='title', how='inner').sort_values('similarity score with target movie', ascending=True)
            target_movie_watched_similarity = target_movie_watched_similarity[:num_similar_items]
   
            # checking if sum of weights is 0
            sum_weights = target_movie_watched_similarity['similarity score with target movie'].sum()

            if sum_weights == 0 :
                predicted_rating = np.average(target_movie_watched_similarity['rating'])
                predicted_rating = round(predicted_rating, 6)
            else:
                predicted_rating = np.average(target_movie_watched_similarity['rating'], weights=target_movie_watched_similarity['similarity score with target movie'])
            
            predicted_rating = round(predicted_rating, 6)
            predict_rating[movie] = predicted_rating
            recommended_movies = dict(sorted(predict_rating.items(), key= lambda item: item[1], reverse=True)[:num_of_recs])
    else:
        recommended_movies = None

    return recommended_movies

# now to pickle, pickle the recommend_movies method
pickle.dump(recommend_movies, open("ml_model.sav", "wb"))