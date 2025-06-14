import pandas as pd
from typing import List, Dict

def clean_and_validate(movies: List[Dict], year: int) -> pd.DataFrame:
    """Clean and validate TMDB movie data.

    This function handles:
    - Removing missing or negative popularity scores
    - Converting vote count to numeric
    - Removing duplicates
    - Validating release dates against the selected year
    - Sorting by popularity descending

    Args:
        movies (List[Dict]): Raw movie records from TMDB API.
        year (int): Year used to validate release dates.

    Returns:
        pd.DataFrame: Cleaned and validated movie data.
    """
    print("\n🔍 Starting data cleaning and validation...")

    df = pd.DataFrame(movies)

    # Drop missing or NaN popularity scores
    missing_popularity = df['popularity'].isnull().sum()
    print(f"Missing popularity values: {missing_popularity}")
    df = df.dropna(subset=['popularity'])

    # Filter out negative popularity values
    df = df[df['popularity'] >= 0]

    # Convert vote_count to numeric (handle any non-numeric entries)
    df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')

    # Drop duplicate entries based on TMDB movie ID
    before_dedup = len(df)
    df = df.drop_duplicates(subset=['id'])
    print(f"Removed {before_dedup - len(df)} duplicate records.")

    # Filter only movies with valid release dates in target year
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
    start_date = f"{year}-01-01"
    end_date = f"{year}-12-31"
    df = df[df['release_date'].between(start_date, end_date)]

    # Sort by popularity descending
    df = df.sort_values(by='popularity', ascending=False).reset_index(drop=True)

    print(f"✅ Cleaned dataset contains {len(df)} movies for {year}")
    return df
