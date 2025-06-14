import pandas as pd

def flag_unreliable_movies(df: pd.DataFrame) -> pd.DataFrame:
    """Flag potentially unreliable movies based on popularity and vote count thresholds.

    A movie is flagged as unreliable if:
    - Its popularity score is in the top 1% (above 99th percentile), and
    - Its vote count is below the 25th percentile of that top 1% subset

    Args:
        df (pd.DataFrame): Cleaned movie dataset.

    Returns:
        pd.DataFrame: DataFrame with an additional column `flagged_as_unreliable` (bool).
    """
    print("\n📊 Flagging unreliable popularity scores...")

    # Compute 99th percentile for popularity
    high_pop_threshold = df['popularity'].quantile(0.99)
    print(f"High popularity threshold (99th percentile): {high_pop_threshold:.2f}")

    # Get top 1% most popular movies
    top_movies = df[df['popularity'] > high_pop_threshold]

    # Compute 25th percentile of vote count in that top 1%
    low_vote_threshold = top_movies['vote_count'].quantile(0.25)
    print(f"Low vote threshold (25th percentile in top 1%): {low_vote_threshold:.0f}")

    # Flag movies meeting both conditions
    df['flagged_as_unreliable'] = (
        (df['popularity'] > high_pop_threshold) &
        (df['vote_count'] < low_vote_threshold)
    )

    print(f"🔎 Flagged {df['flagged_as_unreliable'].sum()} movies as potentially unreliable.")
    return df
