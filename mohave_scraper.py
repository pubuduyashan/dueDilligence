#!/usr/bin/env python3
"""
Mohave County Assessor - Affidavit of Value Search Scraper
Scrapes data for book numbers 100-410 with date range 01/01/2010 to 10/31/2025
Filters by Property Type: Vacant Land
"""

import os
import time
import logging
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MohaveScraper:
    """Scraper for Mohave County Affidavit of Value Search"""

    def __init__(self, output_dir='scraped_data', from_date='01/01/2010', to_date='10/31/2025', property_type='Vacant Land'):
        self.url = 'https://www.mohave.gov/departments/assessor/affidavit-of-value-search/'
        self.output_dir = output_dir
        self.from_date = from_date
        self.to_date = to_date
        self.property_type = property_type
        self.driver = None

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Date range: {self.from_date} to {self.to_date}")
        logger.info(f"Property type: {self.property_type}")

    def setup_driver(self):
        """Initialize Chrome WebDriver with appropriate options"""
        logger.info("Setting up Chrome WebDriver...")

        chrome_options = Options()
        # Run in headless mode (no GUI)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        # Add user agent to avoid detection
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def scrape_book(self, book_number):
        """
        Scrape data for a specific book number

        Args:
            book_number (int): The book number to search for

        Returns:
            pd.DataFrame: DataFrame containing the scraped data, or None if no data found
        """
        logger.info(f"Scraping book number: {book_number}")

        try:
            # Navigate to the page
            self.driver.get(self.url)

            # Wait for page to load
            time.sleep(2)

            # Find and fill the FROM date field
            try:
                from_date_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'fromDate'))
                )
                from_date_input.clear()
                from_date_input.send_keys(self.from_date)
                logger.info(f"Entered from date: {self.from_date}")
            except (TimeoutException, NoSuchElementException) as e:
                logger.warning(f"Could not find 'fromDate' field, trying alternatives: {e}")
                try:
                    # Try by id or other attributes
                    from_date_input = self.driver.find_element(By.ID, 'fromDate')
                    from_date_input.clear()
                    from_date_input.send_keys(self.from_date)
                except NoSuchElementException:
                    logger.warning("No 'from date' field found, continuing without it")

            # Find and fill the TO date field
            try:
                to_date_input = self.driver.find_element(By.NAME, 'toDate')
                to_date_input.clear()
                to_date_input.send_keys(self.to_date)
                logger.info(f"Entered to date: {self.to_date}")
            except NoSuchElementException:
                try:
                    # Try by id or other attributes
                    to_date_input = self.driver.find_element(By.ID, 'toDate')
                    to_date_input.clear()
                    to_date_input.send_keys(self.to_date)
                except NoSuchElementException:
                    logger.warning("No 'to date' field found, continuing without it")

            # Find and select property type from Property Type Code dropdown
            try:
                # Try by name attribute first
                property_type_dropdown = self.driver.find_element(By.NAME, 'propertyTypeCode')
                select = Select(property_type_dropdown)
                select.select_by_visible_text(self.property_type)
                logger.info(f"Selected '{self.property_type}' from Property Type Code dropdown")
            except NoSuchElementException:
                try:
                    # Try by id
                    property_type_dropdown = self.driver.find_element(By.ID, 'propertyTypeCode')
                    select = Select(property_type_dropdown)
                    select.select_by_visible_text(self.property_type)
                    logger.info(f"Selected '{self.property_type}' from Property Type Code dropdown")
                except NoSuchElementException:
                    logger.warning("No 'Property Type Code' dropdown found, continuing without it")
            except Exception as e:
                logger.warning(f"Could not select property type '{self.property_type}': {e}")

            # Find the book input field - trying multiple possible selectors
            try:
                # Try by name attribute
                book_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'book'))
                )
            except TimeoutException:
                try:
                    # Try by id
                    book_input = self.driver.find_element(By.ID, 'book')
                except NoSuchElementException:
                    # Try by other selectors
                    book_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')

            # Clear and input the book number
            book_input.clear()
            book_input.send_keys(str(book_number))
            logger.info(f"Entered book number: {book_number}")

            # Find and click the submit/search button
            try:
                # Try multiple possible button selectors
                submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            except NoSuchElementException:
                try:
                    submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
                except NoSuchElementException:
                    submit_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Search")]')

            submit_button.click()
            logger.info("Clicked submit button")

            # Wait for results to load
            time.sleep(3)

            # Look for the data table
            try:
                table = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'table'))
                )
            except TimeoutException:
                logger.warning(f"No table found for book {book_number}")
                return None

            # Extract table data using pandas
            tables = pd.read_html(self.driver.page_source)

            if not tables:
                logger.warning(f"No data tables found for book {book_number}")
                return None

            # Get the first table (or iterate through tables if multiple)
            df = tables[0]

            # Add metadata columns
            df['book_number'] = book_number
            df['property_type'] = self.property_type
            df['from_date'] = self.from_date
            df['to_date'] = self.to_date
            df['scraped_at'] = datetime.now().isoformat()

            logger.info(f"Successfully scraped {len(df)} rows for book {book_number}")
            return df

        except Exception as e:
            logger.error(f"Error scraping book {book_number}: {e}")
            return None

    def save_data(self, df, book_number):
        """
        Save DataFrame to CSV file

        Args:
            df (pd.DataFrame): DataFrame to save
            book_number (int): Book number for filename
        """
        if df is None or df.empty:
            logger.warning(f"No data to save for book {book_number}")
            return

        filename = f"book_{book_number}.csv"
        filepath = os.path.join(self.output_dir, filename)

        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Saved data to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save data for book {book_number}: {e}")

    def scrape_range(self, start=100, end=410):
        """
        Scrape data for a range of book numbers

        Args:
            start (int): Starting book number (inclusive)
            end (int): Ending book number (inclusive)
        """
        logger.info(f"Starting scrape for books {start} to {end}")

        self.setup_driver()

        success_count = 0
        fail_count = 0

        try:
            for book_num in range(start, end + 1):
                try:
                    df = self.scrape_book(book_num)

                    if df is not None:
                        self.save_data(df, book_num)
                        success_count += 1
                    else:
                        fail_count += 1

                    # Add a small delay between requests to be polite
                    time.sleep(2)

                except Exception as e:
                    logger.error(f"Failed to process book {book_num}: {e}")
                    fail_count += 1
                    continue

                # Log progress every 10 books
                if book_num % 10 == 0:
                    logger.info(f"Progress: {book_num - start + 1}/{end - start + 1} books processed")

        finally:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed")

        logger.info(f"Scraping complete! Success: {success_count}, Failed: {fail_count}")
        return success_count, fail_count

    def create_combined_file(self):
        """Combine all individual CSV files into one master file"""
        logger.info("Creating combined CSV file...")

        csv_files = [f for f in os.listdir(self.output_dir) if f.startswith('book_') and f.endswith('.csv')]

        if not csv_files:
            logger.warning("No CSV files found to combine")
            return

        dfs = []
        for csv_file in csv_files:
            filepath = os.path.join(self.output_dir, csv_file)
            try:
                df = pd.read_csv(filepath)
                dfs.append(df)
            except Exception as e:
                logger.error(f"Error reading {csv_file}: {e}")

        if dfs:
            combined_df = pd.concat(dfs, ignore_index=True)
            combined_filepath = os.path.join(self.output_dir, 'all_books_combined.csv')
            combined_df.to_csv(combined_filepath, index=False)
            logger.info(f"Combined file created: {combined_filepath} ({len(combined_df)} total rows)")


def main():
    """Main execution function"""
    scraper = MohaveScraper(
        output_dir='scraped_data',
        from_date='01/01/2010',
        to_date='10/31/2025',
        property_type='Vacant Land'
    )

    # Scrape books 100-410
    success, failed = scraper.scrape_range(start=100, end=410)

    # Create combined file
    scraper.create_combined_file()

    print("\n" + "="*50)
    print("SCRAPING SUMMARY")
    print("="*50)
    print(f"Successfully scraped: {success} books")
    print(f"Failed to scrape: {failed} books")
    print(f"Property type: {scraper.property_type}")
    print(f"Date range: {scraper.from_date} to {scraper.to_date}")
    print(f"Output directory: {scraper.output_dir}")
    print("="*50)


if __name__ == '__main__':
    main()
