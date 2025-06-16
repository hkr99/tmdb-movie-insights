# 🎬 TMDB Movie Insights

> ⚠️ **Preface:**  
> This project was inspired by a previous take-home assignment for a data engineering role. I aimed to repurpose and improve upon said task to demonstrate similar skills: data ingestion, validation, enrichment, and analysis.

---

A data pipeline that fetches, cleans, enriches, and analyses movie metadata from [The Movie Database (TMDB)](https://www.themoviedb.org/) API.

This project demonstrates:
- API ingestion with pagination and rate limit handling
- Data cleaning and validation logic
- Popularity score reliability analysis
- Genre enrichment via TMDB genre mapping
- Export to clean, readable Excel or JSON outputs

---

##  📌 Features

-  Ingests all English-language movies released in a given year
-  Handles TMDB API pagination and rate limits
- Cleans and validates data (e.g. missing values, duplicates)
- Flags unreliable popularity scores based on vote count percentiles
- Enriches records with human-readable genre names
- Exports to `.xlsx` or `.json` with optional highlighting

---


## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/tmdb-movie-insights.git
cd tmdb-movie-insights
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file at the project root (or copy the example):

```bash
cp .env.example .env
```

Then add your TMDB API key:
```bash
TMDB_API_KEY=your_tmdb_api_key_here
```

---

## ▶️ How to Run the Pipeline

```bash
python main.py
```

| Argument          | Description                            | Default |
| ----------------- | -------------------------------------- | ------- |
| `--year`          | Year of movie releases to fetch        | `2023`  |
| `--output-format` | Output file format (`excel` or `json`) | `excel` |

Examples:
```bash
python main.py --year 2022
python main.py --year 2021 --output-format json
```
---

## 📂 Output

Output files are saved to:
data/

Output columns:
- `title`
- `popularity`
- `vote_count`
- `genres`
- `flagged_as_unreliable`

---

## Future Improvements

- Add additional filtering by genre or vote threshold
- Refactor previous analysis into notebook-based
- Add unit tests
- Add final report

---

## Reflection

I chose to do this project again so I could measure how my design choices and thinking had evolved after having worked in that position, if I was to do the same thing in a limited time frame. Sometimes you don't see how much you are learning until you put yourself up to the same tasks again.
