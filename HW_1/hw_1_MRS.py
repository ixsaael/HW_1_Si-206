# Author: [Ixsaael Hernandez]
# Date: [1-17-2024]
# Assignment: SI-206 HW 1
# Usage: Movie Recommendation System Using AI

import os
import pandas as pd
import json

# Define the base directory (current script location)
base_dir = os.path.dirname(__file__)

# Define file paths
json_files = [os.path.join(base_dir, f"movies_{i}.json") for i in range(1, 5)]
excel_files = [os.path.join(base_dir, f"movies_{i}.xlsx") for i in range(1, 5)]

# Function to load data from JSON files
"""
Load data from a list of JSON files and combine it into a single DataFrame.

Args:
    files (list): List of file names (JSON format).

Returns:
    pandas.DataFrame: A DataFrame containing combined data from all JSON files.
"""
def load_json_data(files):
    movie_data = []
    for file in files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                movie_data.extend(data)
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return pd.DataFrame(movie_data)

# Function to load data from Excel files
"""
Load data from a list of Excel files and combine it into a single DataFrame.

Args:
    files (list): List of file names (Excel format).

Returns:
    pandas.DataFrame: A DataFrame containing combined data from all Excel files.
"""
def load_excel_data(files):
    movie_data = []
    for file in files:
        try:
            df = pd.read_excel(file)
            movie_data.append(df)
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"Error loading {file}: {e}")
    return pd.concat(movie_data, ignore_index=True) if movie_data else pd.DataFrame()

# Function to load all data
"""
Load movie data from both JSON and Excel files and combine into a single DataFrame.

Returns:
    pandas.DataFrame: A DataFrame containing all combined movie data.
"""
def load_all_data():
    json_data = load_json_data(json_files)
    excel_data = load_excel_data(excel_files)
    return pd.concat([json_data, excel_data], ignore_index=True) if not json_data.empty or not excel_data.empty else pd.DataFrame()

# Function to filter movies based on user input
"""
Filter movies based on genre, minimum rating, and release year.

Args:
    movies (pandas.DataFrame): The DataFrame containing movie data.
    genre (str, optional): The genre to filter by (case insensitive). Default is None.
    min_rating (float, optional): The minimum rating to filter by. Default is None.
    release_year (int, optional): The minimum release year to filter by. Default is None.

Returns:
    pandas.DataFrame: A filtered DataFrame containing movies matching the criteria.
"""
def filter_movies(movies, genre=None, min_rating=None, release_year=None):
    if genre:
        movies = movies[movies['genre'].str.contains(genre, case=False, na=False)]
    if min_rating:
        movies = movies[movies['rating'] >= min_rating]
    if release_year:
        movies = movies[movies['release_year'] >= release_year]
    return movies

# Main function
"""
Main function to load data, accept user inputs, and display movie recommendations.
"""
def main():
    # Load all movie data
    movies = load_all_data()

    if movies.empty:
        print("No movie data found. Please check the dataset files.")
        return

    # Display available genres and ask for user input
    print("Available genres:", movies['Genre'].dropna().unique())
    genre = input("Enter a genre (or leave blank to skip): ").strip()

    try:
        min_rating = float(input("Enter a minimum rating (or leave blank to skip): ").strip() or 0)
    except ValueError:
        print("Invalid rating. Defaulting to 0.")
        min_rating = 0

    try:
        release_year = int(input("Enter a minimum release year (or leave blank to skip): ").strip() or 0)
    except ValueError:
        print("Invalid year. Defaulting to 0.")
        release_year = 0

    # Filter and display results
    filtered_movies = filter_movies(movies, genre, min_rating, release_year)
    if filtered_movies.empty:
        print("No movies found matching your criteria.")
    else:
        print("Recommended movies:")
        print(filtered_movies)

if __name__ == "__main__":
    main()


