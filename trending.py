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

    video_data = []
    scroll_pause_time = 2  # Pausing to allow content to load

    while len(video_data) < number:
        videos = driver.find_elements(By.CSS_SELECTOR, 'div.tiktok-559e6k-DivItemContainer.e1aajktk28')
        
        for video in videos:
            video_obj = {}
            try:
                # Find the first child: contains image, like number, description.
                info_wrapper = video.find_element(By.CSS_SELECTOR, "div.e1aajktk17")
                
                # Extract image source from the <img> element
                #img = info_wrapper.find_element(By.CSS_SELECTOR, "img")
                #img_src = img.get_attribute("src")
                
                # Extract the like number (assumed inside a <strong> with these classes)
                like_element = info_wrapper.find_element(By.CSS_SELECTOR, "strong.tiktok-ksk56u-StrongLikes.e1aajktk9")
                if like_element.text:
                    video_obj['Likes'] = like_element.text
                else:
                    video_obj['Likes'] = 'N/A'
                
                # Extract the video description
                # Sometimes the description text is stored in the title attribute
                desc_element = info_wrapper.find_element(By.CSS_SELECTOR, "div.tiktok-1y32mm7-DivVideoDescription.e1aajktk10")
                description = desc_element.get_attribute("title") or desc_element.text
                if description:
                    video_obj['Description'] = description
                    # Extracting hashtags
                    video_obj['Hashtags'] = ",".join(extract_hashtags(description))
                else:
                    video_obj['Description'] = 'N/A'
            except Exception as e:
                print("Error extracting first child data:", e)
                continue
            
            try:
                # Find the second child: contains username and view number.
                author_wrapper = video.find_element(By.CSS_SELECTOR, "div.e1aajktk18")
                
                # Extract username (using the p element with data-e2e attribute)
                username_element = author_wrapper.find_element(By.CSS_SELECTOR, "p[data-e2e='video-user-name']")
                if username_element.text:
                    video_obj['User'] = username_element.text
                else:
                    video_obj['User'] = 'N/A'
                
                # Extract view number (assuming it's inside a span with these classes)
                view_element = author_wrapper.find_element(By.CSS_SELECTOR, "span.tiktok-1cgeagm-SpanLikes.e1aajktk13")
                if view_element.text:
                    video_obj['Views'] = view_element.text
                else:
                    video_obj['Views'] = 'N/A'
            except Exception as e:
                print("Error extracting second child data:", e)
                continue
            
            video_data.append(video_obj)
            
            if len(video_data) >= number:
                break

        # Scrolling down to load more videos
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # Wait for new videos to load

    if quick == True:
        driver.quit()

    return video_data