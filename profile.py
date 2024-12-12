# Import selenium, webdriver-manager and pandas libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import built-in libraries
import time

# Function to scrape user pages
def scrape_user_page_with_selenium(url, driver=None):
    quick = False
    if driver == None:
        # Initializing the WebDriver using webdriver-manager
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")  # Disable GPU (useful for Windows)
        options.add_argument("--no-sandbox")  # Bypass OS security model
        options.add_argument("--disable-dev-shm-usage")  # Overcome resource limitations in Docker
        driver = webdriver.Chrome(service=service, options=options)
        quick = True


    driver.get(url)
    time.sleep(5)  # Waiting for the page to load

    user_data = {}

    # Extracting follower count
    try:
        follower_count = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="followers-count"]').text
        user_data['Follower Count'] = follower_count
    except Exception as e:
        user_data['Follower Count'] = 'N/A'

    # Extracting following count
    try:
        following_count = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="following-count"]').text
        user_data['Following Count'] = following_count
    except Exception as e:
        user_data['Following Count'] = 'N/A'

    # Extracting likes count
    try:
        likes_count = driver.find_element(By.CSS_SELECTOR, 'strong[data-e2e="likes-count"]').text
        user_data['Likes Count'] = likes_count
    except Exception as e:
        user_data['Likes Count'] = 'N/A'

    # Extracting bio
    try:
        bio = driver.find_element(By.CSS_SELECTOR, 'h2[data-e2e="user-bio"]').text
        user_data['Bio'] = bio
    except Exception as e:
        user_data['Bio'] = 'N/A'

    # Extracting username
    try:
        username = driver.find_element(By.CSS_SELECTOR, 'h1[data-e2e="user-title"]').text
        user_data['Username'] = username
    except Exception as e:
        user_data['Username'] = 'N/A'

    if quick == True:
        driver.quit()
    
    return user_data
