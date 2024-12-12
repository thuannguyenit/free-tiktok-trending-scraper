# Import selenium, webdriver-manager and pandas libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import built-in libraries
import time

# Import our own code
from utils import extract_hashtags, remove_hashtags

# Function to scrape trending videos
def scrape_trending_videos_with_selenium(url, number=1, driver=None):
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

    videos = []
    scroll_pause_time = 2  # Pausing to allow content to load

    while len(videos) < number:
        video_description = driver.find_elements(By.CSS_SELECTOR, 'div.tiktok-1anth1x-DivVideoDescription.e1aajktk10')

        for video in video_description[len(videos):]:
            video_data = {}
            description_element = video.find_element(By.XPATH, '..')
            description_text = video.text
            video_data['Description'] = description_text  # Capture description with hashtags

            # Extracting views
            if description_element.find_elements(By.CSS_SELECTOR, 'strong.tiktok-ksk56u-StrongLikes.e1aajktk9'):
                video_data['Views'] = description_element.find_element(By.CSS_SELECTOR, 'strong.tiktok-ksk56u-StrongLikes.e1aajktk9').text
            else:
                video_data['Views'] = 'N/A'

            # Extracting username
            try:
                user_element = description_element.find_element(By.XPATH, '..//a/p[@data-e2e="video-user-name"]')
                video_data['User'] = user_element.text
            except Exception as e:
                video_data['User'] = 'N/A'

            # Extracting likes
            try:
                likes_element = description_element.find_element(By.XPATH, '..//span[contains(@class, "tiktok-10tcisz-SpanLikes") and contains(@class, "e1aajktk13")]')
                video_data['Likes'] = likes_element.text.split()[-1]  # Extract the last part assuming it's the like count
            except Exception as e:
                video_data['Likes'] = 'N/A'

            # Extracting hashtags
            video_data['Hashtags'] = ",".join(extract_hashtags(description_text))

            videos.append(video_data)

            if len(videos) >= number:
                break

        # Scrolling down to load more videos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # Wait for new videos to load

    if quick == True:
        driver.quit()

    return videos