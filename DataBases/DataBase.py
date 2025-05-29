import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from Excel.ExcelInsert import E_Init

class DB:

    engine = create_engine(r"mssql+pyodbc://aaa:1234@DESKTOP-572CNE4/WB41?driver=ODBC+Driver+17+for+SQL+Server")

    SERVER = r"DESKTOP-572CNE4"
    DATABASE = "WB41"
    UID = "aaa"
    PWD = "1234"

    # 정성 정보 , 예보 항목 , 지역항목
    TABLE_NAMES = ("temp_table1" , "temp_table2" , "temp_table3")

    #데이터베이스 초기 설정
    Set_Conn = f"Driver={{SQL Server}};Server={SERVER};Database={DATABASE};UID={UID};PWD={PWD};"
    
    def __init__(self):
        
        if not self.CheckTable():
            E_Init(*self.TABLE_NAMES)
        
        # 테이블 생성 (복합 PK)
        with pyodbc.connect(self.Set_Conn) as conn:
            cursor = conn.cursor()  
            cursor.execute('''
            IF OBJECT_ID('dbo.Recently_Weather', 'U') IS NULL
            CREATE TABLE dbo.Recently_Weather (
                baseDate int,
                baseTime int,
                category VARCHAR(50),
                fcstDate int,
                fcstTime VARCHAR(10),
                fcstValue VARCHAR(100),
                nx int,
                ny int,
                PRIMARY KEY (fcstDate, fcstTime, category , nx , ny)
            )
            ''')

            conn.commit()

    # 테이블 존재여부
    def CheckTable(self):        
        try:
            for table_name in self.TABLE_NAMES:
                with pyodbc.connect(self.Set_Conn) as conn:
                    cursor = conn.cursor()  
                    cursor.execute(f"select Top 1 * from {table_name}")
            return True
        except:
            return False        
    # 모든 지역명 출력 ( 지역이름 )
    def ListRegion(self):
        with pyodbc.connect(self.Set_Conn) as conn:
            cursor = conn.cursor()  
            cursor.execute(f"select [1단계]  , [2단계] from {self.TABLE_NAMES[2]} where [2단계] is Not Null and [3단계] is Null") 
            return cursor.fetchall()         
     
        # 위도 경도 ( 중복 제거 )
        with pyodbc.connect(self.Set_Conn) as conn:
            cursor = conn.cursor()  
            cursor.execute(f"select DISTINCT [격자 X]  , [격자 Y] from temp_table3 where [1단계] is Not Null and [2단계] is Not Null and [3단계] is Null")         
            return cursor.fetchall()         
    # 지역 -> 위도 경도
    def SelectRegion(self , step1 , step2):   

        sql = "SELECT [격자 X] , [격자 Y] from temp_table3 where [1단계] = ? and [2단계] = ? and [3단계] is Null"
        params = (step1, step2)

        with pyodbc.connect(self.Set_Conn) as conn:
            cursor = conn.cursor()  
            cursor.execute(sql , params)    
            
            return cursor.fetchone()
    # 카테고리 코드값 -> 이름 , 단위
    def SelectCategory(self , part , category):
        sql = "SELECT 항목명 , 단위 from temp_table2 where 예보구분 = ? and 항목코드 = ?"
        params = (part, category)

        with pyodbc.connect(self.Set_Conn) as conn:
            cursor = conn.cursor()  
            self.cursor.execute(sql, params)

            return self.cursor.fetchone()   


    # redis에 값이 없을 시 데이터 베이스에서 정보를 가져옴
    # 데이터 정보 가져오기 ( 단기 예보 )
    def SelectWeather(self , step1 , step2):

        nx , ny = self.SelectRegion(step1 , step2)

        sql = "Select category , fcstDate , fcstTime , fcstValue from Weather_Forecast where nx = ? and ny = ? order by fcstdate , fcsttime"
        params = ( nx , ny)

        df = pd.read_sql_query(sql , con = self.engine , params=params)

        grouped = df.groupby(['fcstDate' , 'fcstTime'])

        data = []
        for idx , group in grouped:
            
            row = {}

            row['예상시간'] = f'{group['fcstDate'].iloc[0]} : {group['fcstTime'].iloc[0]}'

            group = group.drop(['fcstDate' , 'fcstTime'], axis=1)

            for idx , (key , value) in group.iterrows():
                row[key] = value
            
            data.append(row)

        return (step1 , step2) , data
        
    # 데이터 정보 가져오기 ( 이전 날씨 )



