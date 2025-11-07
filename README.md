# dueDilligence
An AI automated land due diligence tool

## Project Overview

This project contains tools for automating land due diligence research, including web scraping for property records and assessments.

## Current Features

### Mohave County Assessor Scraper

Automated web scraper for the [Mohave County Assessor's Affidavit of Value Search](https://www.mohave.gov/departments/assessor/affidavit-of-value-search/).

**Features:**
- Scrapes affidavit data for book numbers 100-410
- Saves individual and combined CSV files
- Comprehensive logging and error handling
- Google Drive upload capability

**Quick Start:**

```bash
# Install dependencies
pip install -r requirements.txt

# Test the scraper (books 100-102)
python test_scraper.py

# Run full scraper (books 100-410)
python mohave_scraper.py

# Upload to Google Drive (requires setup)
python upload_to_drive.py
```

**Documentation:**
- See [SCRAPER_README.md](SCRAPER_README.md) for detailed usage instructions
- See [upload_to_drive.py](upload_to_drive.py) for Google Drive integration

## Project Structure

```
.
├── mohave_scraper.py       # Main scraper script
├── test_scraper.py         # Test script for validation
├── upload_to_drive.py      # Google Drive upload helper
├── requirements.txt        # Python dependencies
├── SCRAPER_README.md       # Detailed scraper documentation
└── scraped_data/          # Output directory (created on first run)
```

## Requirements

- Python 3.8+
- Chrome/Chromium browser (auto-installed via webdriver-manager)
- See requirements.txt for Python packages

## Contributing

This is an automated land research tool. Please ensure compliance with website terms of service when scraping.

## License

For educational and authorized use only.
