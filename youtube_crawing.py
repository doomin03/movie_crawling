from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class youtube_select(object):
    def __init__(self, driver_path, MAX_search=3):
        self.url = 'https://www.youtube.com'
        self.driver = webdriver.Chrome(driver_path)
        self.wait = WebDriverWait(self.driver, 10)
        self.media = {}
        self.MAXX_SEARCH = MAX_search
        
            
    def search(self, title):
        highest_similarity = 0.6
        most_similar_data = None
    
        self.driver.get(self.url)
        search_box = self.driver.find_element(By.NAME, 'search_query')
        search_box.send_keys(title)
        search_box.submit()
        
        #//*[@id="chips"]/yt-chip-cloud-chip-renderer[3]
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='chips']/yt-chip-cloud-chip-renderer[3]")))

        # 요소 클릭
        element.click()
        
        for i in range(1, self.MAXX_SEARCH + 1):
            title = self.get_title(i)
            runing_time = self.get_runing(i)
            self.enter_video(i)
            channel = self.get_channel()
            data = self.get_date()
            self.driver.back()
        
            new_data = {'title': title, 'channel': channel, 'runing_time': runing_time, 'data': data}
            similarity_score = self.calculate_similarity(title, new_data)
        
            if similarity_score > highest_similarity:
                highest_similarity = similarity_score
                most_similar_data = new_data
            
        return most_similar_data

    def calculate_similarity(self, title, data):
        title_similarity = self.__similarity_score(title, data['title'])
        return title_similarity

    def get_runing(self, num):
        try:
            runing_time = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#contents > ytd-video-renderer:nth-child(%d) #time-status"%num)))
            return runing_time.text.strip()
        except Exception as e:
            print("영상 길이 크롤링 실패")
            return None
        
    def enter_video(self, num): 
        try:   
            first_video = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#contents > ytd-video-renderer:nth-child(%d) #video-title"%num)))
            first_video.click()
        except Exception as e:
            print("영상 접속 실패")
            
        
    def get_title(self, num):
        try:
            title = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#contents > ytd-video-renderer:nth-child(%d) #video-title > yt-formatted-string"%num)))
            return title.text
        except Exception as e:
            print("제목 크롤링 실패")
            return None
        
    def get_channel(self):
        try:
            channel = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#upload-info > #channel-name")))
            return channel.text
        except Exception as e:
            print("채널 크롤링 실패")
            return None
        
    def get_date(self):
        try:
            button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#description-inner")))
            button.click()
            date = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#info > span:nth-child(3)")))
            
            return date.text
        except Exception as e:
            # button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#description-inner")))
            # button.click()
            # date = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#info > span:nth-child(3)")))
            print("날짜 크롤링 실패")
    

        
    def __levenshtein_distance(self, s1, s2):
        if len(s1) < len(s2):
            return self.__levenshtein_distance(s2, s1)

        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)

        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def __similarity_score(self, s1, s2):
        distance = self.__levenshtein_distance(s1, s2)
        max_length = max(len(s1), len(s2))
        similarity = 1 - distance / max_length
        return similarity

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
            
    
    def web_driver_close(self):
        self.driver.close()