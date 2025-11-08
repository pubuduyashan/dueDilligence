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
from bs4 import BeautifulSoup
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

    def __init__(self, output_dir='../../data/raw/mohave', from_date='01/01/2010', to_date='10/31/2025', property_type='Vacant Land'):
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
            # Use custom ChromeDriver path if it exists, otherwise use ChromeDriverManager
            custom_driver_path = os.path.join(os.path.dirname(__file__), 'chromedriver-win64', 'chromedriver.exe')
            if os.path.exists(custom_driver_path):
                logger.info(f"Using custom ChromeDriver: {custom_driver_path}")
                service = Service(custom_driver_path)
            else:
                logger.info("Using ChromeDriverManager to download driver")
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

            # Switch to the iframe containing the search form
            try:
                iframe = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'iframe1'))
                )
                self.driver.switch_to.frame(iframe)
                logger.info("Switched to iframe")
                time.sleep(1)  # Wait for iframe content to load
            except TimeoutException:
                logger.warning("Could not find iframe, continuing with main page")

            # Select "Book Search" radio button
            try:
                book_search_radio = self.driver.find_element(By.CSS_SELECTOR, 'input[type="radio"][value="Book Search"]')
                self.driver.execute_script("arguments[0].click();", book_search_radio)
                logger.info("Selected 'Book Search' radio button")
                time.sleep(0.5)
            except NoSuchElementException:
                logger.warning("Could not find 'Book Search' radio button")

            # Find and fill the FROM date field (date input type, use JavaScript)
            try:
                from_date_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, 'date_from'))
                )
                # Convert MM/DD/YYYY to YYYY-MM-DD format for date input
                from_date_parts = self.from_date.split('/')
                from_date_formatted = f"{from_date_parts[2]}-{from_date_parts[0]:0>2}-{from_date_parts[1]:0>2}"
                self.driver.execute_script("arguments[0].value = arguments[1];", from_date_input, from_date_formatted)
                logger.info(f"Entered from date: {self.from_date} (formatted: {from_date_formatted})")
            except (TimeoutException, NoSuchElementException) as e:
                logger.warning(f"Could not find 'date_from' field: {e}")
            except Exception as e:
                logger.warning(f"Error setting from date: {e}")

            # Find and fill the TO date field (date input type, use JavaScript)
            try:
                to_date_input = self.driver.find_element(By.NAME, 'date_to')
                # Convert MM/DD/YYYY to YYYY-MM-DD format for date input
                to_date_parts = self.to_date.split('/')
                to_date_formatted = f"{to_date_parts[2]}-{to_date_parts[0]:0>2}-{to_date_parts[1]:0>2}"
                self.driver.execute_script("arguments[0].value = arguments[1];", to_date_input, to_date_formatted)
                logger.info(f"Entered to date: {self.to_date} (formatted: {to_date_formatted})")
            except NoSuchElementException as e:
                logger.warning(f"Could not find 'date_to' field: {e}")
            except Exception as e:
                logger.warning(f"Error setting to date: {e}")

            # Find and select property type from Property Type Code dropdown
            # Map property type names to their values
            property_type_values = {
                'Vacant Land': 'VL',
                'Single Family Residential': 'SF',
                'Commercial/Industrial': 'CI',
                'Agricultural': 'AG',
                'Apartment Building': 'AP',
                'Condo/Townhouse': 'CT',
                'Mobile Home': 'MH',
                '2 - 4 Plex': 'PX',
                'Other': 'OT',
                'All Types': '0'
            }

            try:
                property_type_dropdown = self.driver.find_element(By.NAME, 'property_type_code')
                select = Select(property_type_dropdown)
                # Get the value for the property type
                property_value = property_type_values.get(self.property_type, self.property_type)
                select.select_by_value(property_value)
                logger.info(f"Selected property type '{self.property_type}' (value: {property_value})")
            except NoSuchElementException:
                logger.warning("No 'property_type_code' dropdown found")
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
            time.sleep(5)

            # Check for "No Results Found" message
            try:
                no_results = self.driver.find_element(By.XPATH, "//*[contains(text(), 'No Results Found')]")
                if no_results:
                    logger.warning(f"No results found for book {book_number}")
                    return None
            except NoSuchElementException:
                pass  # Results might exist

            # Look for the results div (not a table - it's a custom div structure)
            try:
                results_container = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'results-table'))
                )
            except TimeoutException:
                logger.warning(f"No results container found for book {book_number}")
                return None

            # Try to set per-page to a high number (to get all results in fewer pages)
            try:
                # Look for the "Per Page" button
                per_page_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Per Page')]")
                if per_page_buttons:
                    per_page_buttons[0].click()
                    time.sleep(1)
                    # Try to select 100 per page if available
                    try:
                        option_100 = self.driver.find_element(By.XPATH, "//button[contains(text(), '100')]")
                        option_100.click()
                        logger.info("Set results to 100 per page")
                        time.sleep(3)  # Wait for page to reload with more results
                    except NoSuchElementException:
                        # Try 50 or 25
                        try:
                            option_50 = self.driver.find_element(By.XPATH, "//button[contains(text(), '50')]")
                            option_50.click()
                            logger.info("Set results to 50 per page")
                            time.sleep(3)
                        except NoSuchElementException:
                            logger.info("Could not increase per-page limit, using default")
            except Exception as e:
                logger.warning(f"Could not change per-page setting: {e}")

            # Collect data from all pages
            all_data = []
            page_num = 1

            while True:
                logger.info(f"Scraping page {page_num} for book {book_number}")

                # Parse the div-based results structure
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                results_div = soup.find('div', {'id': 'results-table'})

                if not results_div:
                    logger.warning(f"No results div found on page {page_num} for book {book_number}")
                    break

                # Find all result rows (they have specific class pattern)
                result_rows = results_div.find_all('div', class_=lambda x: x and 'py-1 p-3 flex' in x)

                if not result_rows:
                    logger.warning(f"No result rows found on page {page_num} for book {book_number}")
                    break

                # Extract data from each row on this page
                page_data = []
                for row in result_rows:
                    try:
                        # Extract parcel number (it's in a div with class "font-bold")
                        parcel_elem = row.find('div', class_='font-bold')
                        if parcel_elem:
                            # Remove the span with the label
                            span = parcel_elem.find('span')
                            if span:
                                span.decompose()
                            parcel = parcel_elem.get_text(strip=True)
                        else:
                            parcel = ''

                        # Extract associated parcels if present
                        associated_parcels = ''
                        associated_elem = row.find('div', class_='leading-4')
                        if associated_elem:
                            # Get text and split by the label
                            associated_text = associated_elem.get_text(separator=', ', strip=True)
                            if 'Associated Parcels:' in associated_text:
                                associated_parcels = associated_text.split('Associated Parcels:')[1].strip()

                        # Find specific data fields by looking for the label spans
                        # and getting only the direct text (not from child elements)
                        property_type = ''
                        reception_number = ''
                        sale_price = ''
                        sale_date = ''

                        # Find all spans with the labels
                        label_spans = row.find_all('span', class_='opacity-70')

                        for span in label_spans:
                            label = span.get_text(strip=True)
                            # Get the parent div
                            parent_div = span.parent

                            if parent_div:
                                # Get only the direct text from this div (excluding children)
                                # by getting all text nodes
                                value = ''
                                for content in parent_div.contents:
                                    if isinstance(content, str):
                                        value += content.strip()

                                # Map the label to the correct field
                                if 'Sale Property Type:' in label:
                                    property_type = value
                                elif 'Reception Number:' in label:
                                    reception_number = value
                                elif 'Sale Price:' in label:
                                    sale_price = value
                                elif 'Sale Date:' in label:
                                    sale_date = value

                        page_data.append({
                            'Sale Parcel': parcel,
                            'Associated Parcels': associated_parcels,
                            'Sale Property Type': property_type,
                            'Reception Number': reception_number,
                            'Sale Price': sale_price,
                            'Sale Date': sale_date
                        })
                    except Exception as e:
                        logger.warning(f"Error parsing row: {e}")
                        continue

                # Add this page's data to all_data
                all_data.extend(page_data)
                logger.info(f"Extracted {len(page_data)} rows from page {page_num}")

                # Check if there's a "Next" button and if it's enabled
                try:
                    next_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Next')]")
                    if next_buttons:
                        next_button = next_buttons[0]
                        # Check if button is actually enabled (not checking class text, using is_enabled())
                        if not next_button.is_enabled() or next_button.get_attribute('disabled') == 'true':
                            logger.info(f"No more pages for book {book_number}")
                            break
                        else:
                            # Click next button
                            next_button.click()
                            logger.info(f"Clicked Next button for page {page_num + 1}")
                            time.sleep(3)  # Wait for next page to load
                            page_num += 1
                    else:
                        logger.info(f"No Next button found, finished scraping book {book_number}")
                        break
                except Exception as e:
                    logger.warning(f"Error checking for Next button: {e}")
                    break

            if not all_data:
                logger.warning(f"No data extracted for book {book_number}")
                return None

            # Create DataFrame
            df = pd.DataFrame(all_data)

            # Add minimal metadata columns
            df['book_number'] = book_number
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
        output_dir='../../data/raw/mohave',
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
