# ( 단기 예보 )API 제공 시간 02:10 부터 3시간 단위 ( 02 : 10  ,  05 : 10  ,  08 : 10  ,  11 : 10  ...)
# ( 초단기 실황) API 제공시간 매시간 + 10분

import requests
from datetime import datetime
import pandas as pd



class Api:    

    def SetTime():
        hour = int(datetime.now().strftime("%H00"))


    def Search(nx , ny):
        url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'        
        params = {
            'serviceKey' : 'vtZFDAfNr+/jUcH8vfYvbRXHk4ZDBvGFoSAB6bh+V2oyQnnzlF2HQOBcK/HV4gOCT3UfgYp/tA5UW9hKJ6WXnA==', 
            'pageNo' : '1', 
            'numOfRows' : '1200', 
            'dataType' : 'JSON', 
            'base_date' : f'{datetime.now().strftime("%Y%m%d")}',   # 현재날짜
            'base_time' : '0200', 
            'nx' : f'{nx}', 
            'ny' : f'{ny}' 
        }

        response = requests.get(url, params=params)

        all = response.json()
        header = all["response"]["header"]

        if header["resultCode"] == "00":
            item = all["response"]["body"]["items"]["item"]
            
            df = pd.DataFrame(item)            
            df.to_json("Test_JSON/item.json", orient='records', force_ascii=False, indent=4)

            grouped = df.groupby(['fcstDate' , 'fcstTime'])
            
            return grouped
        else:
            print(f"Open Api 요청에러 : {header["resultMsg"]}" )
            return None

