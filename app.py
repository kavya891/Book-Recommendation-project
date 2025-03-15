import streamlit as st
import pickle
import numpy as np
import os
from pathlib import Path

# Must be the first Streamlit command
st.set_page_config(
    page_title="Book Recommender System",
    page_icon="📚",
    layout="wide"
)

# Load the pickle files
@st.cache_data
def load_data():
    try:
        base_path = Path(__file__).parent
        popular_df = pickle.load(open(base_path / 'popular.pkl', 'rb'))
        pt = pickle.load(open(base_path / 'pt.pkl', 'rb'))
        books = pickle.load(open(base_path / 'books.pkl', 'rb'))
        similarity_scores = pickle.load(open(base_path / 'similarity_scores.pkl', 'rb'))
        return popular_df, pt, books, similarity_scores
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None

# Load data
popular_df, pt, books, similarity_scores = load_data()

if popular_df is not None:
    # Create tabs
    tab1, tab2 = st.tabs(["Popular Books", "Book Recommendations"])

    # Popular Books Tab
    with tab1:
        st.title("Top Popular Books")
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            with col:
                st.image(popular_df['Image-URL-M'].values[idx])
                st.write(f"**{popular_df['Book-Title'].values[idx]}**")
                st.write(f"*By: {popular_df['Book-Author'].values[idx]}*")
                st.write(f"📊 Ratings: {popular_df['num_ratings'].values[idx]}")
                st.write(f"⭐ Score: {round(popular_df['avg_rating'].values[idx], 2)}")

    # Recommendations Tab
    with tab2:
        st.title("Get Book Recommendations")
        
        user_input = st.text_input("Enter a Book Name", placeholder="e.g., The Da Vinci Code")
        
        if st.button('Get Recommendations', key='recommend_button'):
            if user_input:
                try:
                    index = np.where(pt.index == user_input)[0][0]
                    similar_items = sorted(list(enumerate(similarity_scores[index])), 
                                        key=lambda x: x[1], 
                                        reverse=True)[1:5]
                    
                    cols = st.columns(4)
                    for idx, item in enumerate(similar_items):
                        temp_df = books[books['Book-Title'] == pt.index[item[0]]]
                        with cols[idx]:
                            st.image(temp_df['Image-URL-M'].values[0])
                            st.write(f"**{temp_df['Book-Title'].values[0]}**")
                            st.write(f"*By: {temp_df['Book-Author'].values[0]}*")
                
                except IndexError:
                    st.error("📚 Book not found! Please check the spelling or try another book.")
            else:
                st.warning("⚠️ Please enter a book name.")

# Add CSS for better styling
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput > div > div > input {
        width: 100%;
    }
    div.stMarkdown {
        text-align: center;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)