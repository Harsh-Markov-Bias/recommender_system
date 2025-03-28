import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    movie_overview = data['overview']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path,movie_overview

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters_overview = []
    

    recommended_movie_names.append(movies.iloc[index].title)
    recommended_movie_posters_overview.append(fetch_poster(movies.iloc[index].movie_id))

    for i in distances[1:11]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters_overview.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters_overview


st.header('🎬 Movie Recommender System')

movies = pickle.load(open('pkl/movie_list.pkl', 'rb'))
similarity = pickle.load(open('pkl/similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown 🎥",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters_overview = recommend(selected_movie)

    st.subheader("Selected Movie")

    selected_poster, selected_overview = recommended_movie_posters_overview[0]

    col1, col2 = st.columns([1, 2])  

    with col1:
        st.image(selected_poster, width=200)  

    with col2:
        st.markdown(f"**{recommended_movie_names[0]}**")  
        st.write(selected_overview)  


    st.markdown("<br><hr style='border:1px solid #ddd'><br>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: #df2bf0;'>🍿 Movies You May Like 🎬</h2>", unsafe_allow_html=True)

    for i in range(1, len(recommended_movie_names), 5):  
        cols = st.columns(5)  
        for j in range(5):
            if i + j < len(recommended_movie_names):  
                with cols[j]:
                    movie_poster, _ = recommended_movie_posters_overview[i + j]
                    st.markdown(f"<h4 style='text-align: center; color : #d6a0db'>{recommended_movie_names[i + j]}</h4>", unsafe_allow_html=True)
                    st.image(movie_poster, width=180)


