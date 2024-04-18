import pandas as pd
import pymysql
from youtube_crawing import youtube_select



# def set_price(df):

#     for index, data in df.iterrows():
#         path = r"C:\Users\HAMA\Desktop\crawling\chromedriver-win64\chromedriver.exe"
#         select = youtube_select(path)
#         result_data = select.search(data['m_name'])
#         print(result_data)
#         score = select.get_score()
#         print(score)
#         if score > 0.3:
#             df.at[index, 'm_price'] = 0
#             print("스장")
        
def updata_table():
    conn = pymysql.connect(
    host='localhost',
    port=13309,
    user='admin',
    password='vVYqqRfxkXdM6B5KotBr',
    database='rainbow_tv_test',
    )
    query = "SELECT dmc.`m_name` FROM `dgm_media_change` dmc INNER JOIN `dgm_media_clinic` dmclinic ON dmc.`m_idx` = dmclinic.`m_idx` WHERE dmc.`m_price` IS  NULL;"
    cursor = conn.cursor()
    cursor.execute(query)

# 결과 받아오기
    results = cursor.fetchall()


    for row in results:
        path = r"C:\Users\HAMA\Desktop\crawling\chromedriver-win64\chromedriver.exe"
        select = youtube_select(path)
        select.get_score(row[0])
    conn.close()
 


def main():   
    updata_table()
   

if __name__ == "__main__":
    main()


