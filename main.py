import os
from dotenv import load_dotenv
import argparse
from scripts.ingest import fetch_movies_for_year, fetch_genres
from scripts.clean_validate import clean_and_validate
from scripts.flag_unreliable import flag_unreliable_movies
from scripts.enrich import enrich_with_genres
from scripts.utils import save_dataframe_json, save_dataframe_excel

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise ValueError("❌ Missing TMDB_API_KEY in environment. Please set it in a `.env` file.")

    # Parse CLI arguments
    parser = argparse.ArgumentParser(description="TMDB Movie Insights Pipeline")
    parser.add_argument('--year', type=int, default=2023, help='Year of movie releases to fetch')
    parser.add_argument('--output-format', type=str, choices=['json', 'excel'], default='excel', help='Format to save final output')
    args = parser.parse_args()

    year = args.year
    print(f"\n🚀 Running pipeline for year: {year}")

    # Step 1: Ingest data
    movies = fetch_movies_for_year(api_key, year)
    genres = fetch_genres(api_key)

    # Step 2: Clean and validate
    cleaned_df = clean_and_validate(movies, year)

    # Step 3: Flag unreliable records
    flagged_df = flag_unreliable_movies(cleaned_df)

    # Step 4: Enrich with genre names
    enriched_df = enrich_with_genres(flagged_df, genres)

    # Step 5: Prepare final DataFrame (note: we can include 'vote count' to intuitively see why records are being flagged)
    final_df = enriched_df[['title', 'popularity','vote_count', 'genre(s)', 'flagged_as_unreliable']]

    # Step 6: Save output
    extension = "xlsx" if args.output_format == "excel" else "json"
    output_path = f"data/movie_insights_{year}.{extension}"

    if args.output_format == 'json':
        save_dataframe_json(final_df, output_path)
    else:
        save_dataframe_excel(final_df, output_path)

    print(f"\n✅ Pipeline completed successfully.")

if __name__ == "__main__":
    main()
