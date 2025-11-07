# Form Inspection Guide

## Why Inspect First?

Before running the scraper, we need to verify that the field names in the code match the actual webpage. This prevents errors and wasted time.

## How to Run the Inspector

```bash
# 1. Activate your virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 2. Run the inspection script
python inspect_form.py
```

## What the Inspector Does

1. **Opens the webpage** in a visible browser window
2. **Prints all form fields** with their actual names and IDs
3. **Lists dropdown options** (including "Vacant Land" text)
4. **Saves page source** to `page_source.html`
5. **Takes a screenshot** saved as `form_screenshot.png`
6. **Keeps browser open** so you can manually inspect
7. **Compares** actual field names with what the scraper expects

## What to Look For

The script will show you if these match:

| Scraper Expects | Check Actual Value |
|----------------|-------------------|
| `name='book'` | Does book field have this name? |
| `name='fromDate'` | Does from date field have this name? |
| `name='toDate'` | Does to date field have this name? |
| `name='propertyTypeCode'` | Does dropdown have this name? |
| `'Vacant Land'` | Is this the exact text in dropdown? |

## What to Do Next

### ✅ If Everything Matches
```bash
# The scraper is ready! Test it:
python test_scraper.py
```

### ⚠️ If Names Don't Match

1. **Note the actual field names** from the inspector output
2. **Update `mohave_scraper.py`** with the correct names
3. **Example fix:**

```python
# If inspector shows the book field is actually named 'bookNum':
book_input = WebDriverWait(self.driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'bookNum'))  # Changed from 'book'
)
```

## Manual Verification

When the browser stays open:

1. **Right-click** on the "Book" input field → **Inspect**
2. Look at the HTML: `<input name="?" id="?" />`
3. Verify the `name` and `id` attributes
4. Do the same for date fields and dropdown

## Common Issues

### Issue 1: Field Not Found
```
❌ Could not find 'book' field
```
**Solution:** The field has a different name. Check inspector output.

### Issue 2: Dropdown Text Mismatch
```
❌ Could not select 'Vacant Land'
```
**Solution:** The option text might be "VACANT LAND" (all caps) or "Vacant" or have extra spaces.

### Issue 3: Dynamic Loading
If fields don't appear immediately, the page uses JavaScript to load them. The scraper already has `time.sleep(2)` and `WebDriverWait` to handle this.

## Files Created by Inspector

- **`page_source.html`** - Full HTML of the page (can search for field names)
- **`form_screenshot.png`** - Visual screenshot of the form
- **Console output** - Complete field analysis

## Tips

1. **Run this script first** before running the actual scraper
2. **Keep the console output** for reference
3. **Compare field names carefully** (case-sensitive!)
4. If field names are different, update the scraper before testing

## Next Steps

After inspection:
1. Update scraper if needed → `mohave_scraper.py`
2. Test with small sample → `python test_scraper.py`
3. Verify output looks correct
4. Run full scraper → `python mohave_scraper.py`
