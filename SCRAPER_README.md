# Mohave County Assessor - Affidavit of Value Scraper

This scraper extracts data from the [Mohave County Assessor's Affidavit of Value Search page](https://www.mohave.gov/departments/assessor/affidavit-of-value-search/) for book numbers 100-410.

## Features

- Automated scraping using Selenium WebDriver
- Scrapes data for book numbers 100-410
- Saves individual CSV files for each book
- Creates a combined CSV file with all data
- Comprehensive logging and error handling
- Polite scraping with delays between requests

## Prerequisites

- Python 3.8 or higher
- Chrome/Chromium browser (will be installed automatically via webdriver-manager)

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Run the scraper for all books (100-410)

```bash
python mohave_scraper.py
```

### Run the scraper programmatically

```python
from mohave_scraper import MohaveScraper

# Initialize scraper
scraper = MohaveScraper(output_dir='scraped_data')

# Scrape a range of books
success, failed = scraper.scrape_range(start=100, end=410)

# Create combined file
scraper.create_combined_file()
```

### Scrape a specific range

```python
from mohave_scraper import MohaveScraper

scraper = MohaveScraper()
# Scrape books 100-150 only
scraper.scrape_range(start=100, end=150)
```

## Output

The scraper creates:

1. **Individual CSV files**: `scraped_data/book_XXX.csv` - One file per book number
2. **Combined file**: `scraped_data/all_books_combined.csv` - All data in one file
3. **Log file**: `scraper.log` - Detailed execution log

## Uploading to Google Drive

Since the scraper cannot directly upload to Google Drive, follow these steps:

### Option 1: Manual Upload
1. After scraping completes, navigate to the `scraped_data` folder
2. Upload all CSV files to your Google Drive folder: [Your Drive Folder](https://drive.google.com/drive/folders/1GtUUeBd3Q46FEhlMg87BaBscvqDHC8IE?usp=sharing)

### Option 2: Using Google Drive API (Advanced)

Install additional dependencies:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Use the provided `upload_to_drive.py` script (if created) to automate uploads.

### Option 3: Using rclone (Recommended for automation)
```bash
# Configure rclone with your Google Drive
rclone config

# Sync the scraped_data folder to Google Drive
rclone copy scraped_data/ "your-drive-name:/folder-path/"
```

## Configuration

You can modify the scraper behavior by editing the `mohave_scraper.py` file:

- **Output directory**: Change `output_dir` parameter in `MohaveScraper()`
- **Book range**: Modify `start` and `end` parameters in `scrape_range()`
- **Delays**: Adjust `time.sleep()` values for faster/slower scraping
- **Headless mode**: Comment out `chrome_options.add_argument('--headless')` to see the browser

## Logging

The scraper logs all activities to:
- Console (stdout)
- `scraper.log` file

Log levels:
- **INFO**: Normal operation messages
- **WARNING**: Non-critical issues (e.g., no data found for a book)
- **ERROR**: Critical errors that prevent scraping

## Troubleshooting

### Chrome driver issues
If you encounter Chrome driver errors:
```bash
pip install --upgrade webdriver-manager
```

### Timeout errors
If the site is slow, increase timeout values in the script:
```python
WebDriverWait(self.driver, 20)  # Increase from 10 to 20 seconds
```

### 403 Forbidden errors
The script includes user-agent spoofing. If still blocked, try:
- Adding more realistic headers
- Increasing delays between requests
- Running during off-peak hours

## Notes

- The scraper is designed to be "polite" with 2-second delays between requests
- Progress is logged every 10 books
- Failed scrapes are logged and counted but don't stop the process
- Each book's data includes metadata (book_number, scraped_at timestamp)

## Data Structure

Each CSV file contains:
- Original table columns from the website
- `book_number`: The book number searched
- `scraped_at`: ISO timestamp of when data was scraped

## License

This scraper is for educational and authorized use only. Respect the website's terms of service and robots.txt.
