from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class youtube_select(object):
    def __init__(self, driver_path):
        self.url = 'https://www.youtube.com'
        self.driver = webdriver.Chrome(driver_path)
        self.wait = WebDriverWait(self.driver, 10)
        
    def search(self, name):
        media_data = {'title':None,"runing_time":None,"data":None}
        self.driver.get(self.url)
        search_box = self.driver.find_element(By.NAME, 'search_query')
        search_box.send_keys(name)
        search_box.submit()
        
        title = self.get_title()
        media_data["title"] = title

        runing_time = self.get_runing()
        media_data["runing_time"] = runing_time
        
        self.enter_video()
        date = self.get_date()
        media_data["data"] = date
        
        return media_data
    

    def get_runing(self):
        try:
            runing_time = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#time-status")))
            return runing_time.text.strip()
        except Exception as e:
            print(e)
            return None
        
    def enter_video(self): 
        try:   
            first_video = self.wait.until(EC.element_to_be_clickable((By.ID, "video-title")))
            first_video.click()
        except Exception as e:
            print(e)
        
    def get_title(self):
        try:
            title = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#video-title > yt-formatted-string")))
            return title.text
        except Exception as e:
            print(e)
            return None
        
    def get_date(self):
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.ID, "bottom-row")))
            button.click()
            date = self.driver.find_element_by_css_selector("#info > span:nth-child(3)")
            return date.text
        except Exception as e:
            print(e)
            return None
    
    def web_driver_close(self):
        self.driver.close()
        
        
    
        
        
#/Desktop/crawling/movie_crawling   
        
       
path = r"C:\Users\HAMA\Desktop\crawling\chromedriver-win64\chromedriver.exe"
test = youtube_select(path)
print(test.search("[닥터 체크] 아무튼, 고지혈증 그것이 알고싶다! 고지혈증 한국건강관리협회 대구지부"))
test.web_driver_close()
