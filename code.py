import streamlit as st
import pickle
import pandas as pd
import requests

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ----- Styling -----
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: #E5E5E5;
        }
        h1 {
            color: #D4AF37; /* Gold */
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
        }
        h2 {
            color: #C0C0C0;
            text-align: center;
        }
        h4 {
            color: #F5F5F5;
            text-align: center;
        }
        .movie-title {
            font-weight: 600;
            color: #E5E5E5;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# ----- Title -----
st.markdown("<h1>🎬 CineMatch Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#B0B0B0;'>Discover refined cinematic experiences 🍷</p>",
            unsafe_allow_html=True)


# ----- Fetch Poster Function -----
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=80238c1f12590056867c016d8d0a2729&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "https://via.placeholder.com/500x750?text=No+Image"


# ----- Recommendation Function -----
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# ----- UI Input -----
selected_movie = st.selectbox(
    "🎞️ Select a movie:",
    movies['title'].values
)

# ----- Button Action -----
if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)

    if not names:
        st.warning("No recommendations found. Check your dataset or similarity file.")
    else:
        st.markdown("<h2>✨ Curated Recommendations for You</h2>", unsafe_allow_html=True)
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.markdown(f"<h4>{names[idx]}</h4>", unsafe_allow_html=True)
                st.image(posters[idx], use_container_width=True)
