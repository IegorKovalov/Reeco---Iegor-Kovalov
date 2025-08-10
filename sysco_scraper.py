from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
from datetime import datetime

def setup_driver():
    """Sets up Chrome WebDriver with optimized options for stability and performance.
    
    Configures Chrome options including memory management, stability fixes,
    and UI improvements to handle web scraping operations reliably.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance with stability options.
    """
    # Setup Chrome driver with stability improvementד
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-notifications')
    
    # Memory and stability fixes
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    
    return webdriver.Chrome(options=options)

def initial_auth(driver):
    """Handles initial authentication steps to access Sysco's shopping interface as a guest.

    Navigates through the authentication flow including clicking "Shop Now",
    continuing as guest, entering ZIP code, and starting the shopping session.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance to perform authentication.
        
    Returns:
        bool: True if authentication was successful, False otherwise.
    """
    # Handle initial authentication steps
    try:
        # Navigate to main page
        print("Navigating to Sysco...")
        driver.get("https://www.sysco.com")
        
        # Click "Shop Now"
        print("Clicking Shop Now...")
        shop_now = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Shop Now')]"))
        )
        shop_now.click()
        
        # Click "Continue as Guest"
        print("Continuing as guest...")
        guest_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue as Guest')]"))
        )
        guest_btn.click()
        
        # Enter ZIP code
        print("Entering ZIP code...")
        zip_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-id='initial_zipcode_modal_input']"))
        )
        zip_input.send_keys("97201")
        
        # Click "Start Shopping"
        print("Starting shopping...")
        start_shopping = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Shopping')]"))
        )
        start_shopping.click()
        
        # Add a longer wait after clicking Start Shopping to ensure page loads
        time.sleep(5)
        return True
    
    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return False

def get_all_categories(driver):
    """Retrieves all product categories and their URLs from the Sysco category grid.
    
    Navigates through the category grid to collect category information including
    names, IDs, and URLs for each available product category.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance to extract categories.
        
    Returns:
        list[dict]: List of dictionaries containing category information with keys:
            - 'id': Category identifier string
            - 'name': Human-readable category name
            - 'url': Direct URL to the category page (if successfully captured)
    """
    # Get all category links and their URLs
    try:
        print("Getting categories from grid...")
        
        # Wait for category grid to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "category-grid-container"))
        )
        time.sleep(3)
        
        categories = [
            {'id': 'produce', 'name': 'Produce'},
            {'id': 'meatseafood', 'name': 'Meat & Seafood'},
            {'id': 'bakerybread', 'name': 'Bakery & Breads'},
            {'id': 'dairyeggs', 'name': 'Dairy & Eggs'},
            {'id': 'canneddry', 'name': 'Canned & Dry'},
            {'id': 'frozenfoods', 'name': 'Frozen Foods'},
            {'id': 'beverages', 'name': 'Beverages'},
            {'id': 'equipmentsupplies', 'name': 'Equipment & Supplies'},
            {'id': 'disposables', 'name': 'Disposables'},
            {'id': 'chemicals', 'name': 'Chemicals'}
        ]
        
        # Get URLs for each category
        for category in categories:
            try:
                selector = f"div.category-grid-button span[data-id='lbl_category_app.dashboard.{category['id']}.title']"
                element = driver.find_element(By.CSS_SELECTOR, selector)
                
                # Click element to get URL
                driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(1)
                element.click()
                time.sleep(3)
                
                # Store URL
                category['url'] = driver.current_url
                print(f"Captured URL for {category['name']}: {category['url']}")
                
                # Go back
                driver.back()
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing {category['name']}: {str(e)}")
                category['url'] = None
                
        # Return only categories with valid URLs
        return [cat for cat in categories if cat.get('url')]
        
    except Exception as e:
        print(f"Error getting categories: {str(e)}")
        return []

def get_product_links(driver, retry_count=3):
    """Extracts product links from the current category page with retry logic.
    
    Searches for product cards on the page and extracts their URLs, with
    automatic retry functionality to handle loading issues.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance to extract product links.
        retry_count (int, optional): Number of retry attempts if extraction fails. Defaults to 3.
        
    Returns:
        list[str]: List of product page URLs found on the current page.
    """
    # Get product links with retry logic
    for attempt in range(retry_count):
        try:
            print(f"Getting product links (attempt {attempt + 1}/{retry_count})...")
            
            # Wait for catalog wrapper to load
            WebDriverWait(driver, 15).until(  # Increased wait time
                EC.presence_of_element_located((By.CLASS_NAME, "catalog-cards-wrapper"))
            )
            
            # Additional wait for products to load
            time.sleep(2)
            
            # Get all product cards and extract links
            product_cards = driver.find_elements(By.CSS_SELECTOR, "div.product-card-container")
            
            if not product_cards:
                print(f"No product cards found on attempt {attempt + 1}")
                if attempt < retry_count - 1:
                    print("Refreshing page and retrying...")
                    driver.refresh()
                    time.sleep(5)
                    continue
                else:
                    return []
            
            # Extract links from product cards
            links = []
            for card in product_cards:
                try:
                    link_element = card.find_element(By.CSS_SELECTOR, "a.product-card-link")
                    href = link_element.get_attribute("href")
                    if href:
                        links.append(href)
                except Exception as e:
                    print(f"Could not extract link from product card: {e}")
                    continue
            
            # print(f"Found {len(links)} product links")
            return links
            
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retry_count - 1:
                print("Retrying...")
                time.sleep(3)
                continue
            else:
                print("All attempts failed")
                return []
    
    return []

def extract_product_details(driver, product_link, retry_count=2):
    """Extracts detailed product information from a product page.
    
    Navigates to the specified product page and extracts comprehensive
    product details including SKU, brand, name, packaging, image URL, and description.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance to extract product details.
        product_link (str): URL of the product page to extract information from.
        retry_count (int, optional): Number of retry attempts if extraction fails. Defaults to 2.
        
    Returns:
        dict or None: Dictionary containing product details with keys:
            - 'sku': Product SKU/ID
            - 'brand': Product brand name
            - 'name': Product name
            - 'packaging': Packaging information
            - 'image_url': URL of product image
            - 'description': Product description
        Returns None if extraction fails completely.
    """
    # Extract product details with retry logic
    for attempt in range(retry_count):
        try:
            print(f"Extracting product details (attempt {attempt + 1}/{retry_count})...")
            driver.get(product_link)
            time.sleep(3)  # Wait for page load
            
            # Wait for main product container
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "image-header-info-section"))
            )
            
            # Extract all required fields with error handling for each field
            product_details = {}
            
            # Helper function to safely extract field
            def safe_extract(selector, field_name, get_attribute=None):
                try:
                    element = driver.find_element(By.CSS_SELECTOR, selector)
                    if get_attribute:
                        return element.get_attribute(get_attribute) or "N/A"
                    else:
                        return element.text.strip() or "N/A"
                except Exception as e:
                    print(f"Could not find {field_name}: {e}")
                    return "N/A"
            
            # Extract each field safely
            product_details['sku'] = safe_extract("div[data-id='product_id']", "SKU")
            product_details['brand'] = safe_extract("button[data-id='product_brand_link']", "Brand")
            product_details['name'] = safe_extract("div[data-id='product_name']", "Name")
            product_details['packaging'] = safe_extract("div[data-id='pack_size']", "Packaging")
            product_details['image_url'] = safe_extract("img[data-id='main-product-img-v2']", "Image URL", "src")
            product_details['description'] = safe_extract("div[data-id='product_description_text']", "Description")
            
            # Check if we got at least some data
            valid_fields = sum(1 for value in product_details.values() if value != "N/A")
            if valid_fields >= 3:  # At least 3 fields should be valid
                return product_details
            elif attempt < retry_count - 1:
                print("Not enough valid data, retrying...")
                time.sleep(2)
                continue
            else:
                print("Could not extract sufficient product details")
                return product_details
                
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt < retry_count - 1:
                print("Retrying product extraction...")
                time.sleep(3)
                continue
            else:
                print("All extraction attempts failed")
                return None
    
    return None

def get_total_pages(driver):
    """Determines the total number of pages in the current product category.
    
    Analyzes the search results text to calculate how many pages of products
    are available in the current category.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance on a category page.
        
    Returns:
        int: Total number of pages available (defaults to 1 if calculation fails).
    """
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "catalog-cards-wrapper"))
        )
        
        results_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-id='ss-searchPage-header-label-searchResultsTotalText']"))
        )
        
        results_text = results_element.text
        
        
        numbers = re.findall(r'\d+', results_text)
        total_items = int(numbers[-1])
        total_pages = (total_items + 23) // 24
        print(f"Total items: {total_items}, Pages: {total_pages}")
        return total_pages
        
    except Exception as e:
        print(f"Error getting total pages: {str(e)}")
        return 1
    
def go_to_next_page(driver):
    """Navigates to the next page of products in the current category.
    
    Attempts to click the pagination "next" button to advance to the next
    page of product listings.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance on a category page.
        
    Returns:
        bool: True if navigation was successful, None if it failed.
    """
    print("Navigating to next page...")
    
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.pagination-btn-right"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(1)
        next_button.click()
        print("Success with original selector")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Navigating failed...")

def process_products(driver):
    """Processes all products across all pages within the current category.
    
    Iterates through all pages of the current product category, extracts
    product links from each page, and collects detailed product information.
    Includes error handling and retry logic for failed pages.
    
    Args:
        driver (webdriver.Chrome): Chrome WebDriver instance positioned on a category page.
        
    Returns:
        list[dict]: List of dictionaries containing detailed product information
                   from all successfully processed products in the category.
    """
    # Process products - retry pages instead of giving up
    try:
        all_products = []
        total_pages = get_total_pages(driver)
        
        print(f"Starting to process {total_pages} pages")
        
        category_url = driver.current_url  # Store category page URL
        consecutive_failed_pages = 0  # Track failed pages
        max_failed_pages = 3  # Stop after 3 consecutive failures
        
        for page in range(1, total_pages + 1):
            print(f"\nProcessing page {page} of {total_pages}")
            
            # Get and process products from current page
            product_links = get_product_links(driver)
            
            if not product_links:
                consecutive_failed_pages += 1
                print(f"No products found on page {page} (failure #{consecutive_failed_pages})")
                
                # If we've failed too many times in a row, give up on this category
                if consecutive_failed_pages >= max_failed_pages:
                    print(f"Failed to find products on {consecutive_failed_pages} consecutive pages")
                    print("Giving up on this category")
                    break
                
                # Try to continue to next page anyway - maybe it's just a loading issue
                if page < total_pages:
                    print("Trying to continue to next page anyway...")
                    driver.get(category_url)
                    time.sleep(5)  # Wait longer for page to load
                    
                    if not go_to_next_page(driver):
                        print("Could not navigate to next page either")
                        break
                    else:
                        continue  # Try next page
                else:
                    break  # Last page anyway
            
            else:
                # Reset failure counter when we find products
                consecutive_failed_pages = 0
                print(f"Found {len(product_links)} products on page {page}")
                
                # Process all products on this page
                for index, link in enumerate(product_links, 1):
                    print(f"Processing product {index}/{len(product_links)} on page {page}/{total_pages}")
                    product_details = extract_product_details(driver, link)
                    if product_details:
                        all_products.append(product_details)
            
            # Go to next page if not on last page
            if page < total_pages:
                print("Returning to category page...")
                driver.get(category_url)
                time.sleep(3)  # Wait for category page to load
                
                if not go_to_next_page(driver):
                    print("Could not navigate to next page, stopping here")
                    break
        
        print(f"\nSuccessfully processed {len(all_products)} total products from this category")
        return all_products
        
    except Exception as e:
        print(f"Error processing products: {str(e)}")
        return all_products if 'all_products' in locals() else []

def save_to_csv(products):
    """Saves product data to a CSV file with timestamp.
    
    Creates a CSV file containing all collected product information,
    with filename including current timestamp for uniqueness.
    
    Args:
        products (list[dict]): List of dictionaries containing product information
                              with keys matching CSV fieldnames.
                              
    Returns:
        bool: True if save operation was successful, False otherwise.
    """
    # Save products data to CSV file
    if not products:
        print("No products to save")
        return False
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sysco_products_{timestamp}.csv"
    
    try:
        with open(filename, 'w') as file:
            writer = csv.DictWriter(file, fieldnames=['sku', 'brand', 'name', 'packaging', 'image_url', 'description'])
            writer.writeheader()
            writer.writerows(products)
        print(f"\nData saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
        return False

def main():
    """Main execution function that orchestrates the complete web scraping workflow.
    
    Coordinates the entire scraping process including driver setup, authentication,
    category discovery, product processing, and data saving. Handles cleanup and
    error recovery throughout the process.
    
    The function processes all available categories and collects product information
    until completion, then saves all collected data to a CSV file.
    """
    # Main execution function
    driver = None
    all_products = []
    
    try:
        driver = setup_driver()
        
        # Step 1: Authenticate as guest
        if not initial_auth(driver):
            print("Authentication failed!")
            return
        
        print("Authentication successful!")
        
        # Step 2: Get category URLs 
        categories = get_all_categories(driver)
        if not categories:
            print("No categories found!")
            return
        
        print(f"Found {len(categories)} categories to process")
        
        # Step 3: Process each category until we get 3000+ items
        for category in categories:
            print(f"\nProcessing category: {category['name']}")
            
            # Navigate to category page
            driver.get(category['url'])
            time.sleep(3)
            
            # Get all products from this category
            products = process_products(driver)
            
            if products:
                all_products.extend(products)
                print(f"Collected {len(products)} products from {category['name']}")
                print(f"Total items so far: {len(all_products)}")
                
                # Check if we've reached our goal
                if len(all_products) >= 3000:
                    print("Reached 3000 items target!")
                    break
            else:
                print(f"No products collected from {category['name']}")

        # print("\nFinished processing ALL categories")
        
        # Step 4: Save results
        if all_products:
            save_to_csv(all_products)
            print(f"\nSUCCESS! Processed {len(all_products)} products total")
        else:
            print("\nNo products collected at all")
            
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        
    finally:
        print("Closing browser...")
        if driver:
            try:
                driver.quit()
            except:
                pass  # Ignore errors when closing crashed driver

if __name__ == "__main__":
    main()