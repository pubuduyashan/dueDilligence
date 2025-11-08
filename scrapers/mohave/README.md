# Mohave County Assessor Scraper

Scrapes Affidavit of Value data from the [Mohave County Assessor's website](https://www.mohave.gov/departments/assessor/affidavit-of-value-search/).

## Features
- Scrapes books 100-410
- Filters by property type (default: Vacant Land)
- Date range: 01/01/2010 to 10/31/2025
- Full pagination support (scrapes all pages)
- Saves individual and combined CSV files

## Usage

**Test scraper (books 100-102):**
```bash
cd scrapers/mohave
python test_scraper.py
```

**Run full scraper (books 100-410):**
```bash
cd scrapers/mohave
python scraper.py
```

## Output
Data is saved to `data/raw/mohave/`:
- Individual files: `book_XXX.csv`
- Combined file: `all_books_combined.csv`

For detailed documentation, see [docs/scraper_guide.md](../../docs/scraper_guide.md)
