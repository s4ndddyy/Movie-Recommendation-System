import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

#Getting the directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Loading ratings
ratings = pd.read_csv(
    os.path.join(BASE_DIR, "ml-100k", "u.data"),
    sep="\t",
    names=["user_id", "movie_id", "rating", "timestamp"]
)

#List of genres
genres = [
    "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime",
    "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "War", "Western"
]

#Loading movie details
movies = pd.read_csv(
    os.path.join(BASE_DIR, "ml-100k", "u.item"),
    sep="|",
    encoding="latin-1",
    header=None,
    names=["movie_id", "title", "release_date", "video_release_date", "IMDb_URL"] + genres,
    usecols=[0, 1] + list(range(5, 24))
)

#Merging the data of ratings and movies 
data = pd.merge(ratings, movies, on="movie_id")


#User Movie rating matrix
user_movie_matrix = data.pivot_table(
    index="user_id",
    columns="title",
    values="rating"
)

#Converting to Movie User matrix
movie_user_matrix = user_movie_matrix.T.fillna(0)

#Similarity between movies
movie_similarity = cosine_similarity(movie_user_matrix)

movie_similarity_df = pd.DataFrame(
    movie_similarity,
    index=movie_user_matrix.index,
    columns=movie_user_matrix.index
)


def find_matching_movies(user_input):
    
    #Finds movie titles containing user entered keywords.
    
    keywords = [k.strip().lower() for k in user_input.split(",")]
    matched = []

    for title in movie_similarity_df.index:
        title_lower = title.lower()
        for keyword in keywords:
            if keyword in title_lower:
                matched.append(title)
                break

    return matched


def recommend_movies_by_preferences(user_input, n=5):
    
    #Recommends movies similar to user-entered movies.
    
    matched_movies = find_matching_movies(user_input)

    if not matched_movies:
        return [], []

    similarity_scores = pd.Series(dtype=float)

    for movie in matched_movies:
        similarity_scores = similarity_scores.add(
            movie_similarity_df[movie], fill_value=0
        )

    #Removing already matched movies
    similarity_scores = similarity_scores.drop(matched_movies, errors="ignore")

    top_movies = similarity_scores.sort_values(ascending=False).head(n).index.tolist()

    return matched_movies, top_movies


def get_movies_by_genre(selected_genre, n=None):
    
   #Returns movies belonging to a selected genre.
    
    if selected_genre not in genres:
        return []

    genre_movies = movies[movies[selected_genre] == 1]["title"]

    if n:
        genre_movies = genre_movies.head(n)

    return genre_movies.tolist()


def recommend_movies_in_genre(selected_genre, n=5):
    
    #Recommends similar movies within a genre.
    
    genre_movies = get_movies_by_genre(selected_genre)

    if not genre_movies:
        return []

    similarity_scores = pd.Series(dtype=float)

    for movie in genre_movies:
        if movie in movie_similarity_df.index:
            similarity_scores = similarity_scores.add(
                movie_similarity_df[movie], fill_value=0
            )

    similarity_scores = similarity_scores.drop(genre_movies, errors="ignore")

    return similarity_scores.sort_values(ascending=False).head(n).index.tolist()
