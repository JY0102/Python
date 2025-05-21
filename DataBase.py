


import pyodbc
from Excel.ExcelInsert import E_Init

class DB:

    SERVER = r"DESKTOP-572CNE4\SQLEXPRESS"
    DATABASE = "WB41"
    UID = "aaa"
    PWD = "1234"

    conn = None
    cursor = None

    # 정성 정보 , 예보 항목 , 지역항목
    TABLE_NAMES = ("temp_table1" , "temp_table2" , "temp_table3")

    def __init__(self):
        if self.conn is None:             
            self.conn = pyodbc.connect(
                f"Driver={{SQL Server}};"
                f"Server={self.SERVER};"
                f"Database={self.DATABASE};"
                f"UID={self.UID};"
                f"PWD={self.PWD};"
            )

            self.cursor = self.conn.cursor()
        
        if not self.CheckTable():
            E_Init(*self.TABLE_NAMES)
    
    # 테이블 존재여부
    def CheckTable(self):        
        try:
            for table_name in self.TABLE_NAMES:
                self.cursor.execute(f"select * from {table_name}")
            return True
        except:
            return False        
    # 모든 지역 출력
    def List_Region(self):
        self.cursor.execute(f"select [1단계]  , [2단계] from {self.TABLE_NAMES[2]} where [2단계] is Not Null and [3단계] is Null") 
        
        list_temp = self.cursor.fetchall()        
        for temp in list_temp:
            print(f"{temp[0]} : {temp[1]}")         
    # 지역 -> 위도 경도
    def SelectRegion(self , step1 , step2):   

        sql = "SELECT [격자 X] , [격자 Y] from temp_table3 where [1단계] = ? and [2단계] = ? and [3단계] is Null"
        params = (step1, step2)

        self.cursor.execute(sql , params)    

        return self.cursor.fetchone()
    # 카테고리 코드값 -> 이름 , 단위
    def SelectCategory(self , part , category):
        sql = "SELECT 항목명 , 단위 from temp_table2 where 예보구분 = ? and 항목코드 = ?"
        params = (part, category)

        self.cursor.execute(sql, params)

        return self.cursor.fetchone()



