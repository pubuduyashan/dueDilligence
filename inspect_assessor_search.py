#!/usr/bin/env python3
"""
Assessor Search Page Inspector
Analyzes the Mohave County Assessor Search page structure
URL: https://www.mohave.gov/departments/assessor/assessor-search/
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

def inspect_assessor_search():
    """Inspect the Assessor Search page and print all details"""

    print("\n" + "="*70)
    print("MOHAVE COUNTY ASSESSOR SEARCH PAGE INSPECTOR")
    print("="*70)
    print("URL: https://www.mohave.gov/departments/assessor/assessor-search/")
    print("="*70 + "\n")

    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the page
        url = 'https://www.mohave.gov/departments/assessor/assessor-search/'
        driver.get(url)
        time.sleep(3)

        print("✅ Page loaded successfully!\n")

        # === PAGE TITLE AND DESCRIPTION ===
        print("="*70)
        print("PAGE INFORMATION")
        print("="*70)
        print(f"Title: {driver.title}")

        # Try to find page heading
        try:
            headings = driver.find_elements(By.TAG_NAME, 'h1')
            if headings:
                print(f"Main Heading: {headings[0].text}")
        except:
            pass

        # === SEARCH FORM ANALYSIS ===
        print("\n" + "="*70)
        print("SEARCH FORM STRUCTURE")
        print("="*70 + "\n")

        # Find all forms
        forms = driver.find_elements(By.TAG_NAME, 'form')
        print(f"Number of forms found: {len(forms)}\n")

        for idx, form in enumerate(forms, 1):
            action = form.get_attribute('action')
            method = form.get_attribute('method')
            form_id = form.get_attribute('id')
            form_name = form.get_attribute('name')

            print(f"Form #{idx}:")
            print(f"  ID: {form_id}")
            print(f"  Name: {form_name}")
            print(f"  Action: {action}")
            print(f"  Method: {method or 'GET (default)'}")
            print()

        # === INPUT FIELDS ===
        print("="*70)
        print("INPUT FIELDS")
        print("="*70 + "\n")

        inputs = driver.find_elements(By.TAG_NAME, 'input')

        text_inputs = []
        other_inputs = []

        for inp in inputs:
            input_type = inp.get_attribute('type')
            name = inp.get_attribute('name')
            id_attr = inp.get_attribute('id')
            placeholder = inp.get_attribute('placeholder')
            value = inp.get_attribute('value')

            if input_type in ['text', 'search', 'number', 'date']:
                text_inputs.append({
                    'type': input_type,
                    'name': name,
                    'id': id_attr,
                    'placeholder': placeholder,
                    'value': value
                })
            elif input_type not in ['hidden']:
                other_inputs.append({
                    'type': input_type,
                    'name': name,
                    'id': id_attr,
                    'value': value
                })

        print("Text/Search Input Fields:")
        print("-" * 70)
        if text_inputs:
            for idx, inp in enumerate(text_inputs, 1):
                print(f"\n  Field #{idx}:")
                print(f"    Type: {inp['type']}")
                print(f"    Name: '{inp['name']}' {'✅' if inp['name'] else '❌ EMPTY'}")
                print(f"    ID: '{inp['id']}' {'✅' if inp['id'] else '❌ EMPTY'}")
                if inp['placeholder']:
                    print(f"    Placeholder: '{inp['placeholder']}'")
                if inp['value']:
                    print(f"    Default Value: '{inp['value']}'")
        else:
            print("  ⚠️  No text input fields found")

        print(f"\n  Total text input fields: {len(text_inputs)}")

        print("\n\nOther Input Fields (buttons, checkboxes, etc.):")
        print("-" * 70)
        if other_inputs:
            for idx, inp in enumerate(other_inputs, 1):
                print(f"\n  Field #{idx}:")
                print(f"    Type: {inp['type']}")
                print(f"    Name: '{inp['name']}'")
                print(f"    ID: '{inp['id']}'")
                if inp['value']:
                    print(f"    Value: '{inp['value']}'")
        else:
            print("  No other input types found")

        # === SELECT DROPDOWNS ===
        print("\n" + "="*70)
        print("SELECT DROPDOWNS")
        print("="*70 + "\n")

        selects = driver.find_elements(By.TAG_NAME, 'select')

        if selects:
            for idx, sel in enumerate(selects, 1):
                name = sel.get_attribute('name')
                id_attr = sel.get_attribute('id')

                print(f"Dropdown #{idx}:")
                print(f"  Name: '{name}' {'✅' if name else '❌ EMPTY'}")
                print(f"  ID: '{id_attr}' {'✅' if id_attr else '❌ EMPTY'}")

                try:
                    select_obj = Select(sel)
                    options = select_obj.options
                    print(f"  Number of options: {len(options)}")
                    print(f"  Options:")
                    for opt_idx, opt in enumerate(options):
                        opt_value = opt.get_attribute('value')
                        opt_text = opt.text.strip()
                        selected = opt.is_selected()
                        selected_mark = " [SELECTED]" if selected else ""
                        print(f"    {opt_idx + 1}. Text: '{opt_text}' | Value: '{opt_value}'{selected_mark}")
                except Exception as e:
                    print(f"  ⚠️  Could not read options: {e}")
                print()
        else:
            print("  ⚠️  No dropdown fields found")

        print(f"Total dropdowns: {len(selects)}")

        # === BUTTONS ===
        print("\n" + "="*70)
        print("BUTTONS")
        print("="*70 + "\n")

        buttons = driver.find_elements(By.TAG_NAME, 'button')
        input_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="submit"], input[type="button"]')
        all_buttons = buttons + input_buttons

        if all_buttons:
            for idx, btn in enumerate(all_buttons, 1):
                btn_type = btn.get_attribute('type')
                btn_text = btn.text or btn.get_attribute('value')
                btn_name = btn.get_attribute('name')
                btn_id = btn.get_attribute('id')

                print(f"Button #{idx}:")
                print(f"  Type: {btn_type}")
                print(f"  Text: '{btn_text}'")
                print(f"  Name: '{btn_name}'")
                print(f"  ID: '{btn_id}'")
                print()
        else:
            print("  ⚠️  No buttons found")

        # === TEXTAREAS ===
        print("="*70)
        print("TEXTAREA FIELDS")
        print("="*70 + "\n")

        textareas = driver.find_elements(By.TAG_NAME, 'textarea')
        if textareas:
            for idx, ta in enumerate(textareas, 1):
                name = ta.get_attribute('name')
                id_attr = ta.get_attribute('id')
                placeholder = ta.get_attribute('placeholder')

                print(f"Textarea #{idx}:")
                print(f"  Name: '{name}'")
                print(f"  ID: '{id_attr}'")
                if placeholder:
                    print(f"  Placeholder: '{placeholder}'")
                print()
        else:
            print("  No textarea fields found")

        # === LABELS ===
        print("="*70)
        print("FORM LABELS (helps identify field purpose)")
        print("="*70 + "\n")

        labels = driver.find_elements(By.TAG_NAME, 'label')
        if labels:
            for idx, label in enumerate(labels, 1):
                label_text = label.text.strip()
                label_for = label.get_attribute('for')
                if label_text:
                    print(f"Label #{idx}: '{label_text}' (for: '{label_for}')")
        else:
            print("  No labels found")

        # === SAVE OUTPUTS ===
        print("\n" + "="*70)
        print("SAVING PAGE DATA")
        print("="*70 + "\n")

        # Save page source
        with open('assessor_search_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("✅ Page source saved to: assessor_search_page_source.html")

        # Save screenshot
        try:
            driver.save_screenshot('assessor_search_screenshot.png')
            print("✅ Screenshot saved to: assessor_search_screenshot.png")
        except Exception as e:
            print(f"⚠️  Could not save screenshot: {e}")

        # === JAVASCRIPT DETECTION ===
        print("\n" + "="*70)
        print("JAVASCRIPT ANALYSIS")
        print("="*70 + "\n")

        # Check for common AJAX indicators
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        print(f"Number of script tags: {len(scripts)}")

        # Check if page uses common frameworks
        try:
            has_jquery = driver.execute_script("return typeof jQuery !== 'undefined'")
            print(f"Uses jQuery: {has_jquery}")
        except:
            print("Uses jQuery: Unknown")

        # === SEARCH TYPE DETECTION ===
        print("\n" + "="*70)
        print("SEARCH MECHANISM DETECTION")
        print("="*70 + "\n")

        print("To determine how search works, we need to:")
        print("1. Check if form has an 'action' attribute (traditional form submission)")
        print("2. Look for AJAX calls (modern SPAs)")
        print("3. Check for iframe embeds")
        print()

        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        if iframes:
            print(f"⚠️  Found {len(iframes)} iframe(s) - search might be embedded")
            for idx, iframe in enumerate(iframes, 1):
                src = iframe.get_attribute('src')
                print(f"  Iframe #{idx} src: {src}")
        else:
            print("No iframes detected")

        # === COMPARISON WITH AFFIDAVIT SEARCH ===
        print("\n" + "="*70)
        print("KEY OBSERVATIONS")
        print("="*70 + "\n")

        print("This is the ASSESSOR SEARCH page.")
        print("Compare with the AFFIDAVIT OF VALUE SEARCH page.")
        print()
        print("Differences to note:")
        print("- Different search criteria")
        print("- Different result format")
        print("- May have different field names")
        print()
        print("Review the fields above to understand what can be searched.")

        # === KEEP BROWSER OPEN ===
        print("\n" + "="*70)
        print("🌐 BROWSER KEPT OPEN FOR MANUAL TESTING")
        print("="*70)
        print("\nTest the search manually to see:")
        print("  1. What kind of results appear")
        print("  2. How results are displayed (table? list?)")
        print("  3. If there's pagination")
        print("  4. What search parameters are most useful")
        print("\nPress ENTER when done to close the browser...")
        print("="*70 + "\n")

        input()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nPress ENTER to close...")
        input()

    finally:
        driver.quit()
        print("\n✅ Browser closed.")
        print("="*70)
        print("Review the output above to understand the page structure")
        print("Files saved:")
        print("  - assessor_search_page_source.html")
        print("  - assessor_search_screenshot.png")
        print("="*70 + "\n")


if __name__ == '__main__':
    inspect_assessor_search()
