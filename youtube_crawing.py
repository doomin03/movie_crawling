from difflib import SequenceMatcher
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

class youtube_select(object):


    def __init__(self, MAX_search=2):
        self.url = 'https://www.youtube.com'
        chrome_options  = Options()
        chrome_options.add_argument("--headless")
    
        # 브라우저 설정 최적화
        chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화
        chrome_options.add_argument("--disable-gpu")  # GPU 사용 비활성화
        chrome_options.add_argument("--window-size=1280x1696")  # 창 크기 설정
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # 이미지 로드 비활성화
        # DesiredCapabilities 설정
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['pageLoadStrategy'] = 'eager'

        # 사용자 에이전트 설정 (크롤링 탐지 회피)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

        # Chrome 프로세스 최적화
        chrome_options.add_argument("single-process")  # 단일 프로세스 모드
        chrome_options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 비활성화
        chrome_options.add_argument("--disable-dev-tools")  # 개발자 도구 비활성화
        chrome_options.add_argument("--no-zygote")  # Zygote 비활성

        # 로깅 비활성화 및 자동화 탐지 회피
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("detach", True)
        
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options, desired_capabilities=capabilities )
        self.wait = WebDriverWait(self.driver, 10)
        self.MAX_SEARCH = MAX_search
  

    def search(self, input_title):
        self.highest_similarity = 0
        most_similar_data = None
    
        self.driver.get(self.url)
        search_box = self.driver.find_element(By.NAME, 'search_query')
        search_box.send_keys(input_title)
        search_box.submit()
        
        #//*[@id="chips"]/yt-chip-cloud-chip-renderer[3]
        try:
            video_list_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='chips']/yt-chip-cloud-chip-renderer[3]")))
            video_list_button.click()
        except Exception as e:
            print(e)
        
        for i in range(1, self.MAX_SEARCH + 1):
        
            runing_time = self.get_runing(i)
            if runing_time == 'SHORTS':
                print("shorts video skip")
                continue
            title = self.get_title(i)
            self.enter_video(i)
            data = self.get_date()
            self.driver.back()
        
            new_data = {'title': title,  'runing_time': runing_time, 'data': data}
            similarity_score = self.calculate_similarity(input_title, new_data)
        
            if similarity_score > self.highest_similarity:
                self.highest_similarity = similarity_score
                most_similar_data = new_data
        

        self.driver.quit()
        return most_similar_data

    def calculate_similarity(self, title, data):
        # 두 문자열의 일치하는 부분의 비율 계산
        matching_ratio = self.__calculate_matching_ratio(title, data['title'])
        return matching_ratio

    def get_runing(self, num):
        try:
            runing_time = WebDriverWait(self.driver, 15).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='contents']/ytd-video-renderer[%d]  //*[@id='overlays']/ytd-thumbnail-overlay-time-status-renderer/div[1]/badge-shape //*[@id='text']"%num))
            )
            return runing_time.text
        except Exception as e:
            print(f"영상 길이 크롤링 실패: {e}")
        return None
    def enter_video(self, num): 
        try:   
            first_video = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='contents']/ytd-video-renderer[%d] //*[@id='video-title']"%num)))
            first_video.click()
        except Exception as e:
            print("영상 접속 실패")
            
        
    def get_title(self, num):
        try:
            title = self.wait.until(EC.visibility_of_element_located((By.XPATH,"//*[@id='contents']/ytd-video-renderer[%d]  //*[@id='video-title']/yt-formatted-string"%num)))
            return title.text.strip() 
        except Exception as e:
            print("제목 크롤링 실패")
            return None
    
    def get_date(self):
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#description-inner")))
            button.click()
            date = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#info > span:nth-child(3)")))
            
            return date.text.strip() 
        except Exception as e:
            # button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#description-inner")))
            # button.click()
            # date = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#info > span:nth-child(3)")))
            print("날짜 크롤링 실패")
    

        
    # def __levenshtein_distance(self, s1, s2):
    #     if len(s1) < len(s2):
    #         return self.__levenshtein_distance(s2, s1)

    #     if len(s2) == 0:
    #         return len(s1)

    #     previous_row = range(len(s2) + 1)

    #     for i, c1 in enumerate(s1):
    #         current_row = [i + 1]
    #         for j, c2 in enumerate(s2):
    #             insertions = previous_row[j + 1] + 1
    #             deletions = current_row[j] + 1
    #             substitutions = previous_row[j] + (c1 != c2)
    #             current_row.append(min(insertions, deletions, substitutions))
    #         previous_row = current_row

    #     return previous_row[-1]

    # def __similarity_score(self, s1, s2):
    #     distance = self.__levenshtein_distance(s1, s2)
    #     max_length = max(len(s1), len(s2))
    #     similarity = 1 - distance / max_length
    #     return similarity

    # def __compare_word_pairs(self, pair1, pair2):
    #     similarity_pair1 = self.__similarity_score(pair1[0], pair1[1])
    #     similarity_pair2 = self.__similarity_score(pair2[0], pair2[1])
    #     return similarity_pair1, similarity_pair2
    
    
    # def ouput(self, title, channel, data):
    #     part1 = [title, data['title']]
    #     part2 = [channel, data['channel']]
    #     title_score, channel_score = self.__compare_word_pairs(part1, part2)
    #     score = title_score + channel_score
    #     print(score)
    #     if(score > 1):
    #         return True
    #     else:
    #         return False
    def get_score(self):
        return self.highest_similarity      
      
    def __calculate_matching_ratio(self, s1, s2):
        # SequenceMatcher를 사용하여 두 문자열 간의 일치하는 부분의 비율 계산
        matcher = SequenceMatcher(None, s1, s2)
        return matcher.ratio()  
