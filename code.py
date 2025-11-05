movie_to_search = "The Dark Knight"
recommendations = get_movie_recommendations(movie_to_search, n_recommendations=10)

print(f"Movies similar to '{movie_to_search}':")
for i, movie in enumerate(recommendations, 1):
    print(f"{i}. {movie}")
