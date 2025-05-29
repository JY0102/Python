# 엑셀에서 값 불러오기

class E_Init:

    def __init__(self , table_name1 , table_name2 , table_name3):            
        import pandas as pd

        dfs = pd.read_excel(r"Excel/Init.xlsx", sheet_name=['정성정보', '예보항목' , '지역항목'], engine='openpyxl')
        
        from sqlalchemy import create_engine
        from sqlalchemy.types import VARCHAR

        engine = create_engine("mssql+pyodbc://aaa:1234@DESKTOP-572CNE4/WB41?driver=ODBC+Driver+17+for+SQL+Server")

        column_set = {
            '예보요소' : VARCHAR(50), 
            '정성정보 용어' : VARCHAR(50), 
            '정성정보 의미' : VARCHAR(150),
            }
        dfs["정성정보"].to_sql("temp_table1", con=engine, if_exists="replace", index=False , dtype= column_set )  # 테이블 생성 & 저장

        column_set = {
            '예보구분' : VARCHAR(50),
            '항목코드' : VARCHAR(50),
            '항목명' : VARCHAR(50),
            '단위' : VARCHAR(50)
        }
        dfs["예보항목"].to_sql("temp_table2", con=engine, if_exists="replace", index=False , dtype= column_set )  # 테이블 생성 & 저장

        column_set = {
            '구분' : VARCHAR(50),
            '1단계' : VARCHAR(50),
            '2단계' : VARCHAR(50),
            '3단계' : VARCHAR(50)
        }
        dfs["지역항목"].to_sql("temp_table3", con=engine, if_exists="replace", index=False , dtype= column_set ) 
