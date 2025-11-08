#!/usr/bin/env python3
"""
Test script for Mohave scraper
Tests with just a few book numbers (100-102) to verify functionality
"""

from scraper import MohaveScraper
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Test the scraper with a small range"""

    print("\n" + "="*60)
    print("Testing Mohave Scraper")
    print("="*60)
    print("This will test scraping books 100-102")
    print("Property type: Vacant Land")
    print("Date range: 01/01/2010 to 10/31/2025")
    print("="*60 + "\n")

    # Initialize scraper with test output directory
    scraper = MohaveScraper(
        output_dir='../../data/raw/mohave/test_output',
        from_date='01/01/2010',
        to_date='10/31/2025',
        property_type='Vacant Land'
    )

    # Test with just 3 book numbers
    success, failed = scraper.scrape_range(start=100, end=102)

    # Create combined file
    scraper.create_combined_file()

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Successfully scraped: {success} books")
    print(f"Failed to scrape: {failed} books")
    print(f"Output directory: {scraper.output_dir}")
    print("\nCheck the files in 'test_output' directory")
    print("If the test looks good, run: python mohave_scraper.py")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
