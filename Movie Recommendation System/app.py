import streamlit as st
from recommender import (
    recommend_movies_by_preferences,
    get_movies_by_genre,
    recommend_movies_in_genre,
    genres
)

#Page settings
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🍿",
    layout="centered"
)

st.title("Movie Recommendation System")
st.divider()

#Searching movies
st.subheader("Search by Movie Name")

user_input = st.text_input(
    "Enter a movie name (or multiple, separated by commas):",
    placeholder="e.g. Titanic, Star Wars, Godfather"
)

num_recs = st.slider("Number of recommendations:", 1, 10, 5)

if st.button("Get Recommendations"):
    matched, recommendations = recommend_movies_by_preferences(user_input, num_recs)

    if not matched:
        st.error("No matching movies found.")
    else:
        st.subheader("Matched Movies")
        for movie in matched:
            st.write("•", movie)

        st.subheader("Recommended Movies")
        for i, movie in enumerate(recommendations, 1):
            st.write(f"{i}. {movie}")

st.divider()

#Browsing genres
st.subheader("Browse by Genre")

selected_genre = st.selectbox("Choose a genre:", ["Select"] + genres)
num_genre_recs = st.slider("Top recommendations in this genre:", 1, 10, 5)

if selected_genre != "Select":
    st.subheader(f"Movies in {selected_genre}")
    for movie in get_movies_by_genre(selected_genre):
        st.write("•", movie)

    st.subheader(f"Recommended {selected_genre} Movies")
    recommendations = recommend_movies_in_genre(selected_genre, num_genre_recs)

    if recommendations:
        for i, movie in enumerate(recommendations, 1):
            st.write(f"{i}. {movie}")
    else:
        st.write("No recommendations available.")
