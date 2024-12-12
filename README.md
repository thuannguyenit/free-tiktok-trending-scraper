# TikTok Data Scraper with Python and Selenium

This project uses Selenium to scrape trending TikTok videos, extract user profile data, and count the occurrences of hashtags. The scraped data is saved as CSV files for further analysis.

## Features

- **Scrape Trending Videos**: Collect information about the top trending TikTok videos.
- **Extract User Profiles**: Retrieve data from the profiles of creators associated with trending videos.
- **Hashtag Analysis**: Count and list the occurrences of hashtags from trending videos.
- **Export to CSV**: Save all scraped data to structured CSV files for easy accessibility.

## Prerequisites

Ensure the following are installed on your system:
- Python 3.7 or higher
- Google Chrome browser
- Pip libraries specified in the [Requirements](#requirements)

## Requirements

Install the required Python libraries using pip:

```bash
pip install -r requirements.txt


Usage
-----

1.  **Set Up the WebDriver**The script uses webdriver-manager to automatically install and manage the ChromeDriver.
    
2.  Use the provided script to scrape TikTok data:bashCopy codepython scrape\_tiktok\_data.py
    
3.  **Output**
    
    *   Trending videos data is saved to ./output/trending\_videos\_selenium.csv.
        
    *   Hashtag counts are saved to ./output/hashtags\_counts\_selenium.csv.
        
    *   User profile data is saved to ./output/user\_profile\_selenium.csv.
        

Code Overview
-------------

### Libraries Used

*   **Selenium**: Automates web scraping by controlling a web browser.
    
*   **Webdriver-manager**: Manages and installs the appropriate ChromeDriver version.
    
*   **Pandas**: Processes and saves scraped data as CSV files.
    
*   **Collections.Counter**: Counts occurrences of hashtags.
    

### Functionality

1.  **Trending Videos**
    
    *   URL: https://www.tiktok.com/channel/trending-now?lang=en
        
    *   Number of videos scraped: 5
        
    *   Saved to: trending\_videos\_selenium.csv
        
2.  **Hashtag Counts**
    
    *   Extracted from the trending videos.
        
    *   Saved to: hashtags\_counts\_selenium.csv
        
3.  **User Profiles**
    
    *   URLs are derived from the usernames in trending videos.
        
    *   Profile data scraped and saved to: user\_profile\_selenium.csv
        

Notes
-----

*   Ensure TikTok's language settings match the URL being scraped.
    
*   You may enable headless mode in Selenium for faster scraping by uncommenting the --headless option in the code.
    

Disclaimer
----------

This script is for educational purposes only. Please adhere to TikTok's terms of service and scraping policies when using this script.

