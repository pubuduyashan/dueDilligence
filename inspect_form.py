#!/usr/bin/env python3
"""
Form Field Inspector
This script opens the Mohave webpage and prints all form field details
Run this to see the ACTUAL field names before running the scraper
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

def inspect_form():
    """Inspect the Mohave County form and print all field details"""

    print("\n" + "="*70)
    print("MOHAVE COUNTY FORM INSPECTOR")
    print("="*70)
    print("Opening webpage and analyzing form fields...")
    print("="*70 + "\n")

    # Setup Chrome driver (NOT headless - so you can see it)
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the page
        url = 'https://www.mohave.gov/departments/assessor/affidavit-of-value-search/'
        driver.get(url)

        # Wait for page to load
        time.sleep(3)

        print("✅ Page loaded successfully!\n")
        print("="*70)
        print("FORM FIELD ANALYSIS")
        print("="*70 + "\n")

        # === FIND ALL INPUT FIELDS ===
        print("📝 INPUT FIELDS (text, date, number, etc.):")
        print("-" * 70)
        inputs = driver.find_elements(By.TAG_NAME, 'input')

        input_count = 0
        for inp in inputs:
            input_type = inp.get_attribute('type')
            name = inp.get_attribute('name')
            id_attr = inp.get_attribute('id')
            placeholder = inp.get_attribute('placeholder')
            value = inp.get_attribute('value')

            # Only show relevant fields (not hidden, not submit buttons we don't care about)
            if input_type not in ['hidden', 'submit', 'button'] or name or id_attr:
                input_count += 1
                print(f"\n  Input #{input_count}:")
                print(f"    Type: {input_type}")
                print(f"    Name: '{name}' {'❌ EMPTY' if not name else '✅'}")
                print(f"    ID: '{id_attr}' {'❌ EMPTY' if not id_attr else '✅'}")
                if placeholder:
                    print(f"    Placeholder: '{placeholder}'")
                if value:
                    print(f"    Default Value: '{value}'")

        print(f"\n  Total input fields found: {input_count}")

        # === FIND ALL SELECT DROPDOWNS ===
        print("\n" + "="*70)
        print("📋 SELECT DROPDOWNS:")
        print("-" * 70)
        selects = driver.find_elements(By.TAG_NAME, 'select')

        if not selects:
            print("  ⚠️  No select dropdowns found!")

        for idx, sel in enumerate(selects, 1):
            name = sel.get_attribute('name')
            id_attr = sel.get_attribute('id')

            print(f"\n  Dropdown #{idx}:")
            print(f"    Name: '{name}' {'❌ EMPTY' if not name else '✅'}")
            print(f"    ID: '{id_attr}' {'❌ EMPTY' if not id_attr else '✅'}")

            # Get all options
            try:
                select_obj = Select(sel)
                options = select_obj.options
                print(f"    Options ({len(options)} total):")
                for opt in options:
                    opt_value = opt.get_attribute('value')
                    opt_text = opt.text
                    print(f"      - Text: '{opt_text}' | Value: '{opt_value}'")
            except Exception as e:
                print(f"      ⚠️  Could not read options: {e}")

        print(f"\n  Total dropdowns found: {len(selects)}")

        # === FIND SUBMIT BUTTONS ===
        print("\n" + "="*70)
        print("🔘 SUBMIT BUTTONS:")
        print("-" * 70)

        buttons = driver.find_elements(By.TAG_NAME, 'button')
        input_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="submit"]')
        all_buttons = buttons + input_buttons

        for idx, btn in enumerate(all_buttons, 1):
            btn_type = btn.get_attribute('type')
            btn_text = btn.text or btn.get_attribute('value')
            btn_name = btn.get_attribute('name')

            print(f"\n  Button #{idx}:")
            print(f"    Type: {btn_type}")
            print(f"    Text/Value: '{btn_text}'")
            print(f"    Name: '{btn_name}'")

        # === FIND FORM TAG ===
        print("\n" + "="*70)
        print("📋 FORM DETAILS:")
        print("-" * 70)

        forms = driver.find_elements(By.TAG_NAME, 'form')
        if forms:
            for idx, form in enumerate(forms, 1):
                action = form.get_attribute('action')
                method = form.get_attribute('method')
                form_id = form.get_attribute('id')

                print(f"\n  Form #{idx}:")
                print(f"    Action: {action}")
                print(f"    Method: {method or 'GET (default)'}")
                print(f"    ID: {form_id}")
        else:
            print("  ⚠️  No form tag found (might use AJAX)")

        # === SAVE PAGE SOURCE ===
        print("\n" + "="*70)
        print("💾 SAVING PAGE SOURCE:")
        print("-" * 70)

        with open('page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("  ✅ Saved to: page_source.html")

        # === TAKE SCREENSHOT ===
        try:
            driver.save_screenshot('form_screenshot.png')
            print("  ✅ Screenshot saved to: form_screenshot.png")
        except Exception as e:
            print(f"  ⚠️  Could not save screenshot: {e}")

        # === COMPARISON WITH SCRAPER CODE ===
        print("\n" + "="*70)
        print("🔍 COMPARISON WITH YOUR SCRAPER CODE:")
        print("="*70)
        print("\nYour scraper is looking for these field names:")
        print("  - Book field: name='book' or id='book'")
        print("  - From date: name='fromDate' or id='fromDate'")
        print("  - To date: name='toDate' or id='toDate'")
        print("  - Property type: name='propertyTypeCode' or id='propertyTypeCode'")
        print("  - Property type option text: 'Vacant Land'")
        print("\n⚠️  Compare these with the ACTUAL values printed above!")
        print("    If they don't match, you'll need to update mohave_scraper.py")

        # === KEEP BROWSER OPEN ===
        print("\n" + "="*70)
        print("🌐 BROWSER KEPT OPEN FOR MANUAL INSPECTION")
        print("="*70)
        print("\nThe browser window will stay open so you can:")
        print("  1. Right-click on form fields → Inspect")
        print("  2. Verify the field names manually")
        print("  3. Test the form manually to see how it works")
        print("\nPress ENTER when done inspecting to close the browser...")
        print("="*70 + "\n")

        input()  # Wait for user

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nPress ENTER to close...")
        input()

    finally:
        driver.quit()
        print("\n✅ Browser closed. Review the output above.")
        print("="*70 + "\n")


if __name__ == '__main__':
    inspect_form()
