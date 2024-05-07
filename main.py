import pandas as pd
import pymysql
from youtube_crawing import youtube_select

# path = r"C:\Users\HAMA\Desktop\crawling\chromedriver-win64\chromedriver.exe"
# select = youtube_select()    
# result_data = select.search("[법률사전]무고죄 강화 앞으로의 전망")
# print(result_data)

# def update_table():
#     conn = pymysql.connect(
#     host='localhost',
#     port=13309,
#     user='admin',
#     password='vVYqqRfxkXdM6B5KotBr',
#     database='rainbow_tv_test',
#     )
#     select_query = "SELECT dmc.`m_name` FROM `dgm_media_change` dmc INNER JOIN `dgm_media_clinic` dmclinic ON dmc.`m_idx` = dmclinic.`m_idx` WHERE dmc.`m_price` IS  NULL;"
#     cursor = conn.cursor()
#     cursor.execute(select_query)
#     results = cursor.fetchall()  
#     update_query = "UPDATE `dgm_media_change` SET `m_price` = ? WHERE `m_name` =?;"
#     for row in results:
#         select = youtube_select()
#         score = select.get_score(row[0])
#         if (score > 0.4):
#             cursor.execute(update_query, (0, row[0]))
#     conn.commit()
#     conn.close()

class DB_Tool(object):
    def get_conn(self):
        conn = pymysql.connect(
            host='localhost',
            port=13309,
            user='admin',
            password='vVYqqRfxkXdM6B5KotBr',
            database='rainbow_tv_test',
        )
        return conn
    
    def _select(self, query):
        conn = None
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            if conn:
                conn.close()

    def _updata(self, query, updata):
        conn = None
        try:
            conn = self.get_conn()
            cursor = conn.cursor()
            cursor.execute(query, updata)
            conn.commit()  
        finally:
            if conn:
                conn.close() 


def main():   
    tool = DB_Tool()
    select = youtube_select()
    
    select_query = "SELECT dmc.`m_name` FROM `dgm_media_change` dmc INNER JOIN `dgm_media_clinic` dmclinic ON dmc.`m_idx` = dmclinic.`m_idx` WHERE dmc.`m_price` IS  NULL;"
    select_result = tool._select(select_query)
    
    update_query = "UPDATE `dgm_media_change` SET `m_price` = ? WHERE `m_name` =?;"

    for row in select_result:
        score = select.get_score(row[0])
        if (score > 0.4):
            tool._updata(update_query,(0, row[0]))
        
if __name__ == "__main__":
    main()


