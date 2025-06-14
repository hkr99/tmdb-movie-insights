from typing import Dict, List
import pandas as pd


def map_genre_ids_to_names(genre_ids: List[int], genre_mapping: Dict[int, str]) -> str:
    """Convert a list of genre IDs to a comma-separated string of genre names.

    Args:
        genre_ids (List[int]): Genre ID list for a movie.
        genre_mapping (Dict[int, str]): Map of genre IDs to names.

    Returns:
        str: Comma-separated genre names, or 'Unavailable' if mapping fails.
    """
    if not genre_ids:
        return 'Unavailable'

    genre_names = [genre_mapping.get(genre_id, 'Unavailable') for genre_id in genre_ids]
    return ', '.join(genre_names)


def enrich_with_genres(df: pd.DataFrame, genre_mapping: Dict[int, str]) -> pd.DataFrame:
    """Add a new column with genre names mapped from genre IDs.

    Args:
        df (pd.DataFrame): DataFrame containing a `genre_ids` column.
        genre_mapping (Dict[int, str]): Mapping of genre ID to genre name.

    Returns:
        pd.DataFrame: DataFrame with an added `genres` column.
    """
    print("\n🎭 Enriching movies with genre names...")

    df['genres'] = df['genre_ids'].apply(lambda ids: map_genre_ids_to_names(ids, genre_mapping))
    return df
