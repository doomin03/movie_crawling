import os
import pickle
from datetime import timedelta

import orjson
import requests
import pandas as pd


# def api_requester(station_id, station_name, station_ars_no, sgg_code, start_date, end_date):
def api_requester(args):
    station_id = args[0]
    station_name = args[1]
    station_ars_no = args[2]
    sgg_code = args[3]
    start_date = args[4]
    end_date = args[5]
    
    file_name = f'({start_date} {end_date})_({station_name})_({station_id})_({sgg_code}).csv'
    save_path = os.path.join('/root/Storage/buster/Data/station_used', file_name)
    if os.path.isfile(save_path):
        print("이미 존재")
        return 
    
    url = "https://stcis.go.kr/pivotIndi/indiRgrstyExcelExport.do"
    headers = {'Cookie': 'diEZFA5QTM4uJ8Pz8IL8STPpj6dS1YuMV79Mpp98y3aaAl9KzjnC7FBpalYNE6Hg.amV1c19kb21haW4vc2VydmVyMQ=='}
    payload = {
        "indiCd": "Z01710",
        "indiNm": "노선·정류장 지표(정류장별 이용량)",
        "yearaIncldYn": "",
        "mmIncldYn": "Y",
        "dayIncldYn": "Y",
        "sdIncldYn": "",
        "sggIncldYn": "",
        "emdIncldYn": "",
        "routeIncldYn": "",
        "sttnIncldYn": "Y",
        "rgrstyYn": "Y",
        "pgngYn": "N",
        "siteGb": "P",
        "indiClss": "IC03",
        "indiSel": "IC0304",
        "zoneSd": "",
        "zoneSgg": "",
        "zoneEmd": "",
        "zoneDstrct": "",
        "tcboId": "",
        "excclcAreaCd": "",
        "routeId": "",
        "routeSdCd": "",
        "routeSggCd": "",
        "tcboIdSttn": "08",
        "excclcAreaCdSttn": "11100",
        "sttnId": station_id,
        "sttnSdCd": "",
        "sttnSggCd": sgg_code,
        "areaSelYn": "",
        "daybyTblNm": "DM_RUTBY_USECNT_T",
        "mnbyTblNm": "DM_MMBY_RUTBY_USECNT_T",
        "yrbyTblNm": "",
        "dstrctTblNm": "",
        "mnbyDstrctTblNm": "",
        "yrbyDstrctTblNm": "",
        "hiddenFromDay": "",
        "searchDateGubun": "3",
        "searchAreaGubun": "",
        "searchODAreaGubun": "",
        "searchODAreaGubun_2": "",
        "sttnIdGrp": "",
        "searchFromYear": "2023",
        "searchToYear": "2023",
        "searchFromMonth": "2024-03",
        "searchToMonth": "2024-03",
        "searchFromDay": start_date,
        "searchToDay": end_date,
        "searchSpaceNm": "",
        "searchZoneSd": "",
        "searchZoneSgg": "",
        "searchRouteSpaceNm": "",
        "searchPopZoneSd": "",
        "searchPopZoneSgg": "",
        "searchPopZoneEmd": "",
        "searchSttnSpaceNm": "",
        "searchPopSttnZoneSd": "41",
        "searchPopSttnZoneSgg": "",
        "searchPopSttnZoneEmd": "",
        "popupSearchRouteNo": "",
        "popupSearchSttnNma": "",
        "popupSearchSttnArsno": "",
        "rdStgptSel": "Y",
        "searchODStartSpaceNm": "",
        "searchStgptZoneSd": "",
        "searchStgptZoneSgg": "",
        "searchStgptZoneEmd": "",
        "rdAlocSel": "Y",
        "searchODEndSpaceNm": "",
        "searchAlocZoneSd": "",
        "searchAlocZoneSgg": "",
        "searchAlocZoneEmd": "",
    }
    
    import time
    s = time.time()
    response = requests.request("POST", url, headers=headers, data=payload)
    e = time.time()
    print(e - s)
    
    to_csv(save_path, response.text)
    
def to_pickle(save_path, save_target):
    with open(save_path+'.pickle', "wb") as fw:
        pickle.dump(save_target, fw)
def to_html(save_path, save_target):
    with open(save_path+'.html', "w", encoding='utf-8') as f:
        f.write(save_target)
def to_csv(save_path, save_target):
    with open(save_path, "w", encoding='utf-8') as f:
        f.write(save_target)
        
if __name__ == '__main__':
    data_dir = '/root/Storage/buster/Data'
    
    args = []
    date_list = pd.date_range(start="2023-04-06", end="2024-04-05", freq="5d")
    date_list = [(str(x.date()), str((x+timedelta(days=4)).date())) for x in date_list]
    station_req = open(os.path.join(data_dir, 'route_info', 'station_req.json'), 'rb')
    json_data = orjson.loads(station_req.read())
    
    result = json_data.get('result')
    size = len(result)
    
    station_infos = [(x['sttnId'], x['sttnNm'], x['sttnArsno'], x['sggCd']) for x in result[size // 2:]] # 이건호
    # station_infos = [(x['sttnId'], x['sttnNm'], x['sttnArsno'], x['sggCd']) for x in result[:size // 2]] # 정하민
    count = 0
    for (station_id, station_name, station_ars_no, sgg_code) in station_infos:
        for (start_date, end_date) in date_list:
            if count == 10:
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor() as pool:
                    pool.map(api_requester,args)
                    args = []
                    count = 0
            args.append((station_id, station_name, station_ars_no, sgg_code, start_date, end_date))
            count += 1