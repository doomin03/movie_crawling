import pandas as pd
from youtube_crawing import youtube_select



def set_price(df):

    for index, data in df.iterrows():
        path = r"C:\Users\HAMA\Desktop\crawling\chromedriver-win64\chromedriver.exe"
        select = youtube_select(path)
        result_data = select.search(data['m_name'])
        score = select.get_score()    
        if score < 0.2:
            continue    
        df.at[index, 'm_price'] = 0

def main():
    df = pd.read_csv(r"C:\Users\HAMA\Desktop\crawling\movie_crawling\data\dgm_media_NULL_clinic.csv")
    set_price(df)

if __name__ == "__main__":
    main()
