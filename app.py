import time
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def clean_title(title):
    # Replace or remove problematic characters
    return title.replace('\U0001f4af', '')  # Replace with an empty string

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.youtube.com/@PW-Foundation/videos")

channel_title = driver.find_element(By.XPATH, '//yt-formatted-string[contains(@class, "ytd-channel-name")]').text
handle = driver.find_element(By.XPATH, '//yt-formatted-string[@id="channel-handle"]').text
subscriber_count = driver.find_element(By.XPATH, '//yt-formatted-string[@id="subscriber-count"]').text

# Add a delay to ensure page elements are loaded
time.sleep(3)

thumbnails_boxes = driver.find_elements(By.XPATH, '//a[@id="thumbnail"]/yt-image/img')
views_boxes = driver.find_elements(By.XPATH, '//div[@id="metadata-line"]/span[1]')
titles_boxes = driver.find_elements(By.ID, "video-title")
links_boxes = driver.find_elements(By.ID, "video-title-link")

print("Number of titles found:", len(titles_boxes))
print("Number of views found:", len(views_boxes))
print("Number of thumbnails found:", len(thumbnails_boxes))
print("Number of links found:", len(links_boxes))

posting_times = []

metadata_boxes = driver.find_elements(By.XPATH, '//div[@id="metadata-line"]')

for metadata in metadata_boxes[:5]:
    try:
        # Locate the posting time element within the metadata
        posting_time_element = metadata.find_element(By.XPATH, './/span[@class="inline-metadata-item style-scope ytd-video-meta-block"][contains(text(), "ago")]')
        posting_times.append(posting_time_element.text)
    except NoSuchElementException:
        posting_times.append("Posting time not found")


videos = []
for title, view, thumb, link, post_time in zip(titles_boxes[:5], views_boxes[:5], thumbnails_boxes[:5], links_boxes[:5], posting_times):
    decoded_title = clean_title(title.text)
    print("Current Title:", decoded_title)
    # ... (rest of the loop)
    video_dict = {
        'title': decoded_title,
        'views': view.text,
        'thumbnail': thumb.get_attribute('src'),
        'link': link.get_attribute('href'),
        'posting_time': post_time
    }
    videos.append(video_dict)

pprint(videos)

# Close the driver
driver.quit()