import pandas as pd
import plotly.express as px
from preswald import connect, get_df, query, text, table, plotly, sidebar, image, button

connect() 
df = get_df("data/netflix_titles.csv") 

sql = "SELECT show_id, title, director FROM 'data/netflix_titles.csv' WHERE type = 'TV Show' AND release_year = 2021"
filtered_df = query(sql, "data/netflix_titles.csv")

sql2 = "SELECT title, country, release_year FROM 'data/netflix_titles.csv' WHERE type = 'TV Show' AND release_year IN (2010, 2020) AND country = 'United States'"
filtered_df2 = query(sql2, "data/netflix_titles.csv")

sidebar("## Menu")

button("Show TV Shows 2021")
button("Show US Shows 2010 & 2020")
button("Type Distribution")
button("Rating Distribution")
button("Movie Duration Trend")
button("Top Countries")

text("# Netflix Data Explorer")
text("### TV Shows Released in 2021")
table(filtered_df, title="Filtered Netflix Movies (2015+)")

text("### US Movies Released in 2010 and 2020")
table(filtered_df2, title="Filtered US Movies (2010–2020)")

text("## Record Type Distribution")
type_count_plot = px.histogram(
    df,
    x="type",
    title="Distribution of Netflix Titles by Type",
    category_orders={"type": df["type"].value_counts().index.tolist()}
)
plotly(type_count_plot)

text("## Content Rating Distribution")
rating_plot = px.histogram(
    df,
    x="rating",
    title="Distribution of Ratings",
    category_orders={"rating": df["rating"].value_counts().index.tolist()}
)
plotly(rating_plot)

text("## Movie Duration by Release Year")
df_movies = df[df["type"] == "Movie"].copy()
df_movies["duration_int"] = df_movies["duration"].str.extract(r'(\d+)').astype(float)
fig = px.scatter(
    df_movies.dropna(subset=["duration_int", "release_year"]),
    x="release_year",
    y="duration_int",
    title="Movie Duration Over the Years",
    labels={"duration_int": "Duration (minutes)", "release_year": "Release Year"},
    color="rating"
)
plotly(fig)

text("## Top 10 Countries by Content Count")
top_countries = df["country"].dropna().str.split(", ").explode().value_counts().nlargest(10).reset_index()
top_countries.columns = ["country", "count"]
fig = px.bar(top_countries, x="country", y="count", title="Top 10 Countries by Netflix Content")
plotly(fig)
