import pandas as pd
from youtube_crawing import youtube_select



def set_price(df):

    for index, data in df.iterrows():
        path = r"C:\Users\HAMA\Desktop\crawling\chromedriver-win64\chromedriver.exe"
        select = youtube_select(path)
        result_data = select.search(data['m_name'])
        print(result_data)
        score = select.get_score()
        print(score)
        if score > 0.3:
            df.at[index, 'm_price'] = 0
            print("스장")
        




def main():
    df = pd.read_csv(r"C:\Users\HAMA\Desktop\crawling\test\movie_crawling\data\test_data\test1.csv")
    set_price(df)
    df.to_csv(r"C:\Users\HAMA\Desktop\crawling\movie_crawling\data\dgm_media_NULL_clinic_modified.csv", index=False)

if __name__ == "__main__":
    main()


