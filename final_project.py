import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Function to scrape anime movie data from MyAnimeList
def scrape_anime_movies():
    url = "https://myanimelist.net/topanime.php?type=movie"  # Top anime movies list
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch data")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    anime_list = []

    # Try to find the table with anime movie listings
    for row in soup.find_all("tr", class_="ranking-list"):
        # Find title
        title_tag = row.find("h3", class_="hoverinfo_trigger")
        title = title_tag.text.strip() if title_tag else "No Title Found"

        # Find score
        score_tag = row.find("span", class_="score-label")
        score = float(score_tag.text.strip()) if score_tag else None

        # Find number of members
        members_tag = row.find("span", class_="members")
        if members_tag:
            # Strip unwanted characters and convert to an integer
            members = members_tag.text.replace(",", "").strip()
            members = int(members) if members.isdigit() else None
        else:
            members = None

        anime_list.append({"Title": title, "Score": score, "Members": members})

    return pd.DataFrame(anime_list)


# Scrape anime movies
df = scrape_anime_movies()

# Check the first few rows of the data
print(df.head())

# Perform EDA if data is available
if not df.empty:
    print("\nBasic Info:")
    print(df.info())

    print("\nSummary Statistics:")
    print(df.describe())

    # Data Cleaning
    df.dropna(inplace=True)  # Remove missing values

    # Data Visualization
    plt.figure(figsize=(10, 5))
    sns.histplot(df["Score"], bins=10, kde=True)
    plt.title("Distribution of Anime Movie Ratings")
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.show()  # This ensures the plot is shown

    plt.figure(figsize=(12, 6))
    sns.scatterplot(data=df, x="Members", y="Score", alpha=0.7)
    plt.title("Popularity vs Score")
    plt.xlabel("Number of Members")
    plt.ylabel("Score")
    plt.show()  # This ensures the plot is shown

