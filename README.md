# Reeco - Iegor Kovalov

## Sysco Product Scraper

A Python web scraper that extracts product information from Sysco's online catalog using Selenium WebDriver and BeautifulSoup.

## Features

- **Guest Access**: Automatically handles guest authentication flow
- **Location-Based**: Uses Oregon ZIP code (97201) for product availability
- **Multi-Category**: Scrapes products from all available categories
- **Retry Logic**: Handles failures with automatic retry mechanisms
- **Data Export**: Saves collected data to timestamped CSV files
- **Error Handling**: Robust error handling and recovery

## Requirements

```bash
pip install selenium beautifulsoup4 webdriver-manager
```

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

3. Download ChromeDriver and ensure it's in your PATH

## Usage

Run the scraper:
```bash
python sysco_scraper.py
```

The scraper will:
1. Navigate to Sysco.com
2. Complete guest authentication
3. Discover all product categories
4. Extract product details from each category
5. Save results to `sysco_products_YYYYMMDD_HHMMSS.csv`

## Data Fields

The scraper extracts the following product information:
- **SKU**: Product identifier
- **Brand**: Product brand name
- **Name**: Product name
- **Packaging**: Package size/type information
- **Image URL**: Product image URL
- **Description**: Product description

## Configuration

- **ZIP Code**: Oregon ZIP 97201 (can be modified in `initial_auth()`)
- **Target Items**: Stops at 3000+ items (configurable in `main()`)
- **Retry Attempts**: 3 attempts per page, 2 attempts per product

## Categories Processed

- Produce
- Meat & Seafood
- Bakery & Breads
- Dairy & Eggs
- Canned & Dry
- Frozen Foods
- Beverages
- Equipment & Supplies
- Disposables
- Chemicals

## Error Handling

- **Page Load Failures**: Automatic retry with page refresh
- **Missing Elements**: Graceful handling with "N/A" values
- **Navigation Issues**: Multiple fallback strategies
- **ChromeDriver Crashes**: Safe cleanup and recovery

## Output

Creates CSV file with format: `sysco_products_YYYYMMDD_HHMMSS.csv`

## Assignment Requirements

✅ **Language**: Python with Selenium and BeautifulSoup  
✅ **Target**: 3000+ items from 3+ categories  
✅ **Location**: Oregon-based account (ZIP 97201)  
✅ **Data Fields**: All 6 required fields captured  
✅ **Export**: Clean CSV format  
✅ **Code Quality**: Well-documented and readable

## Technical Notes

- Uses Chrome WebDriver with stability optimizations
- Implements retry logic for reliability
- Handles dynamic content loading
- Respects website structure and rate limits
