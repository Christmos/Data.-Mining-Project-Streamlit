import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# To set a webpage title, header and subtitle
st.set_page_config(page_title = "Movies analysis",layout = 'wide')
st.header("📊Interactive Dashboard for Data Mining Streamlit Project")
st.subheader("Exmaples of using various widgets on the sidebar")


#read in the file
movies_data = st.cache_data(pd.read_csv)("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
movies_data.info()
# movies_data = movies_data.dropna()
movies_data['success'] = movies_data["gross"] > movies_data['budget']
movies_data.rating = movies_data.rating.replace('Unrated', 'Not Rated')

# Creating sidebar widget filters from movies dataset
year_list = movies_data['year'].unique().tolist()
score_rating = movies_data['score'].unique().tolist()
genre_list = movies_data['genre'].unique().tolist()
country_list = movies_data['country'].unique().tolist()
rating_list = movies_data['rating'].unique().tolist()
success_list = movies_data['success'].unique().tolist()


# Add the filters. Every widget goes in here
with st.sidebar:
    st.write("Select a range the movie score")
    new_score_rating = st.slider(label = "Choose a score:",
                                  min_value = 1.0,
                                  max_value = 10.0,
                                 value = (6.0,9.0))
    #create a radio widget 
    new_success = st.radio("Is it successful movie?", success_list)
    
    st.write("Select your preferred realised year")
    #create a selectbox option that holds all unique years
    new_year = st.slider('Choose a Year', min_value = 1980,
                                  max_value = 2024, value = (2000,2010))

    st.write("Select your preferred movie country")
    #create a multiselect option that holds company
    new_country_list = st.multiselect('Choose movie country:', country_list, default = ['United Kingdom', 'United States'])

    st.write("Select your preferred movie rating")
    #create a singleselect option that holds rating
    new_rating_list = st.selectbox('Choose a rating:', rating_list)
    
    st.write("Select your preferred movie genre")
    #create a segmented control widget that holds genre
    new_genre_list = st.segmented_control('Choose Genre:', genre_list,  selection_mode="multi",default = ['Drama', 'Adventure'])


#Configure the slider widget for interactivity
score_info = (movies_data['score'].between(*new_score_rating))
year_info = (movies_data['year'].between(*new_year))

#Configure the selectbox and multiselect widget for interactivity
filtering = (movies_data['rating'] == new_rating_list) & (movies_data['country'].isin(new_country_list)) & (movies_data['genre'].isin(new_genre_list)) & score_info & year_info & (movies_data['success'] == new_success)

# if st.checkbox('Show dataframe'):
#    st.write(movies_data)

# Visualization section

col1, col2, col3 = st.columns([3,3, 4])
col4, col5 = st.columns([4,6])

with col1:
    st.write("""🎥 Movies""")
    movies_update = movies_data[filtering][['name', 'star', 'score']]
    # movies_update = movies_update.reset_index()
    st.dataframe(movies_update.nlargest(columns='score', n=50), width = 400, hide_index=True)

with col2:
    st.write("""📽️Movie Votes Over Time""")
    st.line_chart(movies_data[filtering].groupby('year')['votes'].sum().reset_index(), x='year', y='votes', color='#ffaa0088')


with col3:
    st.write("""💸Relationship between budgets and ratings""")
    fig = px.scatter(movies_data[filtering],
    x="budget", y="score", size="gross", color="country", hover_name="name")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

with col4:
    st.write("""🎭Top Stars""")
    st.bar_chart(movies_data[filtering].groupby('star')['score'].mean().reset_index().nlargest(columns='score', n=20), x = 'star', y = 'score', color ="#ffaa0088")
    
with col5:
    st.write("""🎞️Top directors""")
    st.bar_chart(movies_data[filtering].groupby('director')['score'].mean().round(2).reset_index().nlargest(columns='score', n=15), x='score', y='director', horizontal=False, color='#7cb6fc')



