from fastapi import FastAPI
from DataBases.DataBase import DB
from Alarm import worker
import threading
import redis
import json

#http://127.0.0.1:8000

# uvicorn main:app --reload
# main -> 파일 이름
# app -> 변수 이름
# reload -> 코드 수정시 자동 반영

<<<<<<< HEAD
# reids 의 max memory 는 512MB 로 지정
=======
print("test2 branch")
>>>>>>> 168ceec56f0bb5e570f2ad333b3842d7878eb380

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

ip = '220.90.180.114'
# r = redis.Redis(host=ip, port=6379, decode_responses=True)
db = DB()

# 데몬스레드 = 백그라운드 스레드
t = threading.Thread(target=worker, daemon=True)
t.start()


try:
    pong = r.ping()
    print("Redis 연결 성공:", pong)
except Exception as e:
    print("Redis 연결 실패:", e)


@app.get("/wb41/weather/info")
def Get_Weather(step1 : str , step2 : str):
    
    try:
        key = f"('{step1}', '{step2}')"

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
            raise ValueError("data 값이 없습니다.")
        
    except Exception as e:
            return {"Result": False , "data" : e}
    
def InsertRedis(step1 , step2):
        
    key , value = db.SelectWeather(step1 , step2)    

    print(f'{key}')
    r.set(f'{key}', json.dumps(value), ex=10800)  # 3시간 유효

    return json.loads(r.get(f'{key}'))