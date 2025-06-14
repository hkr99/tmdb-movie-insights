import requests
import time
from typing import Dict, List, Tuple

BASE_URL = "https://api.themoviedb.org/3"

def fetch_data(url: str, params: Dict) -> Dict:
    """Fetch data from TMDB API with retry on rate limit.

    Args:
        url (str): The API endpoint URL.
        params (Dict): Parameters for the API request.

    Returns:
        Dict: Parsed JSON response.

    Raises:
        HTTPError: If the request fails with non-200 and non-429 status code.
    """
    while True:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limit exceeded. Retrying after 1 second...")
            time.sleep(1)
        else:
            response.raise_for_status()

def get_movies_by_date_range(api_key: str, start_date: str, end_date: str) -> Tuple[List[Dict], int]:
    """Fetch all movies in a given date range with English as original language.

    Args:
        api_key (str): TMDB API key.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        Tuple[List[Dict], int]: List of movies and total count.
    """
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": api_key,
        "language": "en-US",
        "sort_by": "release_date.desc",
        "include_adult": False,
        "include_video": False,
        "primary_release_date.gte": start_date,
        "primary_release_date.lte": end_date,
        "with_original_language": "en",
        "page": 1
    }

    movies = []
    total_results_count = 0

    while True:
        data = fetch_data(url, params)
        if not data["results"]:
            break
        movies.extend(data["results"])
        total_results_count += len(data["results"])

        if params["page"] < data["total_pages"]:
            params["page"] += 1
            time.sleep(0.1)
        else:
            break

    return movies, total_results_count

def fetch_movies_for_year(api_key: str, year: int) -> List[Dict]:
    """Fetch all movies in a year by splitting into quarterly date ranges.

    Args:
        api_key (str): TMDB API key.
        year (int): Year to fetch movies for.

    Returns:
        List[Dict]: List of movie records.
    """
    quarters = [
        (f"{year}-01-01", f"{year}-03-31"),
        (f"{year}-04-01", f"{year}-06-30"),
        (f"{year}-07-01", f"{year}-09-30"),
        (f"{year}-10-01", f"{year}-12-31"),
    ]

    movies = []
    for start, end in quarters:
        quarter_movies, _ = get_movies_by_date_range(api_key, start, end)
        movies.extend(quarter_movies)

    return movies

def fetch_genres(api_key: str) -> Dict[int, str]:
    """Fetch movie genres from TMDB API.

    Args:
        api_key (str): TMDB API key.

    Returns:
        Dict[int, str]: Mapping of genre IDs to names.

    Raises:
        HTTPError: If the request fails.
    """
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": api_key, "language": "en-US"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    genres = response.json().get("genres", [])
    return {genre["id"]: genre["name"] for genre in genres}
