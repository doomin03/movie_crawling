import os
import time
import random
from tempfile import mkdtemp

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from pytube import YouTube
from pytube.exceptions import AgeRestrictedError
from pytube.exceptions import LiveStreamError
from pytube.exceptions import VideoUnavailable

def web_driver_options():
    chrome_option_object = webdriver.ChromeOptions()
    chrome_option_object.add_argument('--headless')
    chrome_option_object.add_argument('--no-sandbox')
    chrome_option_object.add_argument("--disable-gpu")
    chrome_option_object.add_argument("--window-size=1280x1696")
    chrome_option_object.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    chrome_option_object.add_argument("single-process")
    chrome_option_object.add_argument("--disable-dev-shm-usage")
    chrome_option_object.add_argument("--disable-dev-tools")
    chrome_option_object.add_argument("--no-zygote")
    chrome_option_object.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_option_object.add_argument(f"--data-path={mkdtemp()}")
    chrome_option_object.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_option_object.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_option_object.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_option_object.add_experimental_option("useAutomationExtension", False)
    chrome_option_object.add_experimental_option("detach", True)
    return chrome_option_object

def web_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=web_driver_options())
    return driver

def time_controller(s_range:int, e_range:int):
    sec = random.uniform(s_range, e_range)
    time.sleep(sec)

def download_video(video_url, file_name):
    file_path = f"/root/Storage/Data/data/{file_name}"
    if os.path.isdir(file_path):
        print(video_url, "이미 다운로드 받은 동영상 입니다.")
        return
    
    try:
        yt = YouTube(video_url)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        yt.streams.filter(adaptive=True, file_extension='mp4').first().download(output_path=file_path)
        print(video_url, '동영상 다운로드 완료!')

    except AgeRestrictedError:
        print(video_url, "이 동영상은 연령 제한이 걸려있습니다. 로그인이 필요할 수 있습니다.")
    except LiveStreamError:
        print(video_url, "이 동영상은 라이브 스트리밍 중입니다. 다운로드할 수 없습니다.")
    except VideoUnavailable:
        print(video_url, "이 동영상은 삭제되었거나 비공개로 설정되어있습니다. 다운로드할 수 없습니다.")

    
def main(keyword):
    url = f'https://www.youtube.com/results?search_query={keyword}'
    driver = web_driver()
    driver.get(url)   
    
    watch_btn = driver.find_element(By.XPATH, '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/div/ytd-search-header-renderer/div[1]/yt-chip-cloud-renderer/div/div[2]/iron-selector/yt-chip-cloud-chip-renderer[3]/yt-formatted-string')
    watch_btn.click()
    
    scroll_count = 0
    while True:
        if scroll_count > 1000:
            break
        try:
            driver.find_element(By.XPATH, '//*[@id="message"]').text
            break
        except NoSuchElementException:
            driver.execute_script("window.scrollBy(0, 1000);")
            scroll_count += 1
    
    time.sleep(5)
    for section_idx in range(1, 40+1):
        for content_idx in range(1, 20+1):
            try:
                content = driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[{section_idx}]/div[3]/ytd-video-renderer[{content_idx}]')
            except NoSuchElementException:
                continue
            
            title = content.find_element(By.ID, 'video-title').get_attribute('title')
            condition1 = '시간' in title
            condition2 = 'Hour' in title
            condition3 = 'hour' in title
            condition4 = '음악' in title
            condition5 = 'Music' in title
            condition6 = 'music' in title
            condition7 = '강아지 리믹스' in title
            if condition1 or condition2 or condition3 or condition4 or condition5 or condition6 or condition7:
                continue
            
            link = content.find_element(By.ID, 'thumbnail').get_attribute('href')
            watch = "https://www.youtube.com/watch?v=" in link
            shorts = "https://www.youtube.com/shorts/" in link
            if watch:
                video_code = link.replace('https://www.youtube.com/watch?v=', '')
                video_code = video_code.split('&')[0]
            elif shorts:
                video_code = link.replace('https://www.youtube.com/shorts/', '')
            
            download_video(video_url=link, file_name=video_code)
            
            
if __name__ == '__main__':
    # 유튜브 검색어
    keyword = '강아지'
    main(keyword)