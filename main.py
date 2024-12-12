# Import selenium, webdriver-manager and pandas libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from collections import Counter

# Import our own code
from trending import scrape_trending_videos_with_selenium
from profile import scrape_user_page_with_selenium

# Initializing the WebDriver using webdriver-manager
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU (useful for Windows)
options.add_argument("--no-sandbox")  # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")  # Overcome resource limitations in Docker
driver = webdriver.Chrome(service=service, options=options)

# URL for the page
trending_videos_url = 'https://www.tiktok.com/channel/trending-now?lang=en'
number_of_videos = 5
trending_videos = scrape_trending_videos_with_selenium(trending_videos_url, number_of_videos, driver)

# Convert to DataFrame and save to CSV
# (for easier conversion and better accessibility)
output_trending_file = './output/trending_videos_selenium.csv'
df_videos = pd.DataFrame(trending_videos)
df_videos.to_csv(output_trending_file, index=False)
print(f'Data scraped and saved to {output_trending_file}')

# List of hashtags with occurrences of each value
hashtags = []

# List of user page URLs to scrape
user_page_urls = []
for v in trending_videos:
    user_page_urls.append('https://www.tiktok.com/@' + v['User'])
    hashtags = hashtags + v['Hashtags'].split(",")

# Convert to DataFrame and save to CSV
hashtags_counts = list(Counter(hashtags).items())
output_hashtags_file = './output/hashtags_counts_selenium.csv'
df_hashtags = pd.DataFrame(hashtags_counts, columns=['Hashtag', 'Count'])
df_hashtags.to_csv(output_hashtags_file, index=False)
print(f'Data scraped and saved to {output_hashtags_file}')

# Scrape data for each user page
user_data_list = []
for url in user_page_urls:
    user_data = scrape_user_page_with_selenium(url, driver)
    user_data['URL'] = url  # Add URL to the data for reference
    user_data_list.append(user_data)
    
# Convert to DataFrame and save to CSV
output_profile_file = './output/user_profile_selenium.csv'
df_user = pd.DataFrame(user_data_list)
df_user.to_csv(output_profile_file, index=False)
print(f'Data scraped and saved to {output_profile_file}')

driver.quit()