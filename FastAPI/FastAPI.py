import redis
from fastapi import FastAPI
import json
from WeatherManagement import Weather


# uvicorn main:app --reload
# main -> 파일 이름
# app -> 변수 이름
# reload -> 코드 수정시 자동 반영

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

@app.get("/weather")
def Get_Weather(step1 : str , step2 : str):
    
    key = f"('{step1}','{step2}')"

    cached = r.get(key)
    
    if cached:
        data = json.loads(cached)
        print('redis')
    else:
        data = InsertRedis(step1 , step2)
        print('insert')

    if data:
        return {"Result": True, "data": data}
    else:
        return {"Result": False}

    
def InsertRedis(step1 , step2):
    
    weather = Weather()
    key , value = weather.Search("서울특별시" , "중구")
   
    r.set(key, json.dumps(value), ex=10800)  # 3시간 유효