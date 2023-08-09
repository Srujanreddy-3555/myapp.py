import streamlit as st
import pandas as pd
primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
# Load the movies dataset
movies = pd.read_csv('./movies.csv')

# Load the ratings dataset
ratings = pd.read_csv('./ratings.csv')

def recommend_movies(genre, threshold, N):
    genre_movies = movies[movies['genres'].str.contains(genre)]

    review_counts = ratings['movieId'].value_counts().rename('review_count')
    genre_movies = genre_movies.merge(review_counts, left_on='movieId', right_index=True)
    genre_movies = genre_movies[genre_movies['review_count'] >= threshold]

    average_ratings = ratings.groupby('movieId')['rating'].mean().rename('average_rating')
    genre_movies = genre_movies.merge(average_ratings, left_on='movieId', right_index=True)
    movies_sorted = genre_movies.sort_values(by='average_rating', ascending=False)

    recommended_movies = movies_sorted.head(N)
    return recommended_movies[['movieId', 'title', 'average_rating']]


# create Streamlit app
def main():
    # Page title
    st.title("Movie Recommendation System")

    # Genre input
    genre = st.text_input("Enter the genre:")

    # Minimum review threshold input
    threshold = st.slider("Enter the minimum review threshold:", min_value=0, max_value=500, step=10)

    # Number of recommendations input
    N = st.slider("Enter the number of recommendations:", min_value=1, max_value=10, step=1)

    # Recommend movies button
    if st.button("Recommend Movies"):
        recommended_movies = recommend_movies(genre, threshold, N)
        st.write(recommended_movies)

if __name__ == '__main__':
    main()
