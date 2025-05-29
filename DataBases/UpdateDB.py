from OpenApi import Api

# 데이터 프레임 -> 데이터 베이스로 이동
from sqlalchemy import create_engine
# 데이터 프레임
import pandas as pd
## 성능 측정용 
# from datetime import datetime
##

# 비동기
import asyncio

engine = create_engine(r"mssql+pyodbc://aaa:1234@DESKTOP-572CNE4/WB41?driver=ODBC+Driver+17+for+SQL+Server")

error_Location = []
# 함수 선언부

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# 필요없는 컬럼거르기
def Filter(group):
    filtered_df = group[~group['category'].isin(['UUU', 'VVV', 'VEC', 'WAV'])]
    return filtered_df
# 코드 값 -> 문자열
def CodeToString(data):        
    name , unit = SelectCategory( '단기예보' , data['category'] )

    if unit == '코드값':
        if name == '하늘상태':
            match data['fcstValue']:
                case '1': unit = '맑음'
                case '3': unit = '구름 많음'
                case '4': unit = '흐림'
        elif name == '강수형태':
            match data['fcstValue']:
                case '0': unit = '없음'
                case '1': unit = '비'
                case '2': unit = '비/눈'
                case '3': unit = '눈'
                case '4': unit = '소나기'
        return name , unit
    else :        
        if not data['fcstValue'].isdigit():
            unit = ''
        return name , f'{data['fcstValue']}{unit}'
def SelectCategory(part , category):
    sql = "SELECT 항목명 , 단위 from temp_table2 where 예보구분 = ? and 항목코드 = ?"
    params = (part, category)

    df = pd.read_sql_query(sql  , con = engine , params= params)
    row = df.iloc[0]
    return row.iloc[0] , row.iloc[1]

# 모든 위도 경도 값 출력
def ListRegionLocation():    
    sql = "select DISTINCT [격자 X]  , [격자 Y] from temp_table3 where [1단계] is Not Null and [2단계] is Not Null and [3단계] is Null"   
    df = pd.read_sql_query(sql  , con = engine)   

    locations = []

    for idx, row in df.iterrows():
        locations.append((row.iloc[0] , row.iloc[1]))

    return locations  
# 정보 저장 ( 비동기 )
async def InsertInfo(location):

    try:
        grouped = await Api.Search(*location)

        if not grouped:
            error_Location.append(location)
            print(f"API 정보 없음: {location}")        
            return

        dfs = []
        print(f'{int(location[0])}, {int(location[1])} 시작')

        for name ,group in grouped:
            group = Filter(group)
            
            for idx , row in group.iterrows():

                key , value = CodeToString(row)

                group.loc[idx, 'category'] = key
                group.loc[idx, 'fcstValue'] = value

            dfs.append(group)

        merged = pd.concat(dfs , ignore_index= True)

        await asyncio.get_running_loop().run_in_executor(
            None, 
            lambda: merged.to_sql("Recently_Weather", con=engine, if_exists="append", index=False)
        )

        print(f'{location} 끝', flush=True)
    except Exception as e:
        print(f'{location} Error : {e}')
# 비동기 세팅
async def Recently():
    
    tasks = []

    locations = ListRegionLocation()

    for location in locations:
        tasks.append(asyncio.create_task(InsertInfo(location)))

    print("병렬 run 시작")  

    # 병렬 진행 
    # -> 오류 발생시 error_Location 에 등록후 순차적으로 진행
    if tasks:
        await asyncio.gather(*tasks)

    print("순차 run 시작")  
    # 순차진행
    for location in error_Location:    
        await InsertInfo(location)


# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# 비동기 시작
def Run():
    
    asyncio.run(Recently()) 

    sql = 'Select * from Recently_Weather order by nx , ny , fcstDate , fcstTime'
    df = pd.read_sql_query(sql , con = engine)
    # 최신화 데이터 테이블 -> 원본 데이터 테이블 병합
    # 약 3 ~ 4초 소요
    df.to_sql("Weather_Forecast" , con = engine , if_exists="replace", index=False )

