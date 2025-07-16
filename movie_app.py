import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="🎬 Movie Ratings Analysis", layout="wide")
sns.set(style="whitegrid")

# ✅ Initial Movie Ratings Dataset
initial_data = {
    "user_id": [1, 2, 3, 1, 2, 4, 5, 3, 4, 5],
    "movie": [
        "Inception", "Inception", "Inception",
        "Avengers", "Avengers", "Titanic",
        "Titanic", "Interstellar", "Interstellar", "Joker"
    ],
    "genre": [
        "Sci-Fi", "Sci-Fi", "Sci-Fi",
        "Action", "Action", "Romance",
        "Romance", "Sci-Fi", "Sci-Fi", "Drama"
    ],
    "rating": [5, 4, 5, 4, 3, 5, 4, 5, 4, 3]
}

# Store dataset in session_state (so it updates dynamically)
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(initial_data)

df = st.session_state.df

st.title("🎬 Interactive Movie Ratings Analyzer")

st.subheader("📊 Current Dataset")
st.dataframe(df)

# ✅ User input form
st.sidebar.header("➕ Add a New Rating")

with st.sidebar.form("add_rating_form"):
    user_id = st.number_input("👤 User ID", min_value=1, step=1)
    movie_name = st.text_input("🎥 Movie Name")
    genre = st.selectbox("🎭 Genre", ["Action", "Drama", "Sci-Fi", "Romance", "Comedy"])
    rating = st.slider("⭐ Rating", 1, 5, 3)
    
    submit = st.form_submit_button("Add Rating")

# ✅ Add new rating to dataset dynamically
if submit:
    new_row = {"user_id": user_id, "movie": movie_name, "genre": genre, "rating": rating}
    st.session_state.df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    st.success(f"✅ Added: {movie_name} (Rating: {rating})")
    st.rerun()  # Refresh the dashboard


# ✅ Popular Genres
st.subheader("🎭 Popular Genres")
genre_counts = df['genre'].value_counts()
fig1, ax1 = plt.subplots(figsize=(4,4))
plt.pie(genre_counts, labels=genre_counts.index, autopct="%1.1f%%", colors=sns.color_palette("pastel"))
plt.title("Most Popular Genres")
st.pyplot(fig1)

# ✅ Top Rated Movies
st.subheader("🏆 Top Rated Movies")
top_movies = df.groupby('movie')['rating'].mean().sort_values(ascending=False)
fig2, ax2 = plt.subplots(figsize=(6,3))
sns.barplot(x=top_movies.values, y=top_movies.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Average Rating")
ax2.set_title("Top Rated Movies")
st.pyplot(fig2)

# ✅ Most Active Users
st.subheader("👥 Most Active Users")
active_users = df['user_id'].value_counts()
fig3, ax3 = plt.subplots(figsize=(6,3))
sns.barplot(x=active_users.index.astype(str), y=active_users.values, palette="coolwarm", ax=ax3)
ax3.set_xlabel("User ID")
ax3.set_ylabel("Number of Ratings")
ax3.set_title("Most Active Users")
st.pyplot(fig3)

st.info("💡 Tip: Add a new rating from the sidebar and watch the charts update!")
