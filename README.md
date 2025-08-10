# Reeco - Iegor Kovalov
# Sysco Product Scraper

A Python web scraper that extracts product information from Sysco's online catalog using Selenium WebDriver.

## Features

* **Guest Access**: Automatically handles guest authentication flow
* **Location-Based**: Uses Oregon ZIP code (97201) for product availability  
* **Multi-Category**: Scrapes products from all available categories
* **Retry Logic**: Handles failures with automatic retry mechanisms
* **Data Export**: Saves collected data to timestamped CSV files
* **Error Handling**: Robust error handling and recovery
* **Pagination Support**: Automatically navigates through multiple pages per category

## Requirements

* Python 3.7+
* Chrome browser installed
* ChromeDriver (handled automatically with webdriver-manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/IegorKovalov/Reeco---Iegor-Kovalov.git
cd Reeco---Iegor-Kovalov
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **Optional**: If you encounter ChromeDriver issues, install webdriver-manager:
```bash
pip install webdriver-manager
```

## Usage

Run the scraper:
```bash
python sysco_scraper.py
```

The scraper will:
1. Navigate to Sysco.com
2. Complete guest authentication with ZIP code 97201
3. Discover all product categories
4. Extract product details from each category (with pagination)
5. Save results to `sysco_products_YYYYMMDD_HHMMSS.csv`

## Data Fields

The scraper extracts the following product information:
* **SKU**: Product identifier
* **Brand**: Product brand name  
* **Name**: Product name
* **Packaging**: Package size/type information
* **Image URL**: Product image URL
* **Description**: Product description

## Configuration Options

You can modify these settings in the code:
* **ZIP Code**: Change in `initial_auth()` function (default: 97201)
* **Target Items**: Modify stopping condition in `main()` (default: 3000+)
* **Retry Attempts**: Adjust in function parameters (default: 3 per page, 2 per product)

## Categories Processed

* Produce
* Meat & Seafood  
* Bakery & Breads
* Dairy & Eggs
* Canned & Dry
* Frozen Foods
* Beverages
* Equipment & Supplies
* Disposables
* Chemicals

## Error Handling & Reliability

* **Page Load Failures**: Automatic retry with page refresh
* **Missing Elements**: Graceful handling with "N/A" values
* **Navigation Issues**: Multiple fallback strategies for pagination
* **ChromeDriver Crashes**: Safe cleanup and recovery
* **Consecutive Page Failures**: Stops after 3 consecutive failed pages per category
* **Memory Management**: Chrome options optimized for stability

## Output Format

Creates CSV file with timestamp: `sysco_products_YYYYMMDD_HHMMSS.csv`

Sample output:
```csv
sku,brand,name,packaging,image_url,description
12345,Brand Name,Product Name,Case of 24,https://...,Product description
```

## Assignment Requirements ✅

* **Language**: Python with Selenium ✅
* **Target**: 3000+ items from 10 categories ✅  
* **Location**: Oregon-based account (ZIP 97201) ✅
* **Data Fields**: All 6 required fields captured ✅
* **Export**: Clean CSV format with timestamps ✅
* **Code Quality**: Well-documented with comprehensive error handling ✅

## Technical Implementation

* **WebDriver**: Chrome with optimized stability options
* **Wait Strategy**: Explicit waits with WebDriverWait for reliability
* **Retry Logic**: Multiple retry layers for pages and individual products
* **Memory Management**: Configured Chrome options for long-running scrapes
* **Pagination**: Automatic detection and navigation through product pages
* **Data Validation**: Ensures minimum data quality before saving

## Troubleshooting

**Common Issues:**
* **ChromeDriver not found**: Install webdriver-manager or ensure ChromeDriver is in PATH
* **Timeout errors**: Increase wait times in WebDriverWait calls
* **Memory issues**: Chrome options include memory management flags
* **Authentication failures**: Check if Sysco.com structure has changed

**Performance Tips:**
* Run during off-peak hours for better reliability
* Monitor memory usage for large scraping sessions
* Check output CSV periodically to ensure data quality
