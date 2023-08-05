import streamlit as st
import pandas as pd
import requests

new_df = pd.read_pickle("movies.pkl")

similarity = pd.read_pickle("similarity.pkl")


movies_list = new_df["title"].values

st.title("Movie recommender system")

my_movie = st.selectbox("Movie name",movies_list)


def fetch_poster(movie_id):

    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1Y2Q2ZDgzZjU5OGY5YzJkZDczNTFkNTU5NjM4MDMyOSIsInN1YiI6IjY0YjRkOWU1Nzg1NzBlMDBlMzNiYzhkZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.D4mn7A1cz3cPAVa7fKzI0Jiyfh_PLBelqPRvznXSxYM"
    }

    response = requests.get(url, headers=headers).json()

    return "https://image.tmdb.org/t/p/original/"+response["poster_path"]




def recommended_movies(movie):
    m_index = new_df[new_df.title.str.lower() == movie.lower()].index[0]
    distances = similarity[m_index]
    distances_sorted = sorted(enumerate(distances),reverse=True,key=lambda x:x[1])[1:6]
    movies = []
    posters = []
    for x in distances_sorted:
        movies.append(new_df.iloc[x[0]]["title"])
        posters.append(fetch_poster(new_df.iloc[x[0]]["id"]))    
        
    return movies, posters


if st.button('Recommend'):
    movies,posters = recommended_movies(my_movie)
    #    for movie,poster in zip(similar_movies[0], similar_movies[1]):
    #       st.write(movie)
    #       st.image(poster,width=50)
    
    col1,col2,col3,col4,col5 = st.columns(5)

    count = 0
    for col in (col1,col2,col3,col4,col5):
        with col:
            st.subheader(movies[count])
            st.image(posters[count],width=120)
        count += 1    


    # with col1:
    #     st.text(movies[0])
    #     st.image(posters[0],width=150)
    # with col2:
    #     st.text(movies[1])
    #     st.image(posters[1],width=150)
    # with col3:
    #     st.text(movies[2])
    #     st.image(posters[2],width=200)
    # with col4:
    #     st.text(movies[3])
    #     st.image(posters[3],width=200)
    # with col5:
    #     st.text(movies[4])
    #     st.image(posters[4],width=200)

    
       