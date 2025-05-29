
# from datetime import datetime

from DataBases.DataBase import DB
import json

db = DB()

key , value = db.SelectWeather('울산광역시' , '남구')







# nx = 102
# ny = 84
# sql = "Select category , fcstDate , fcstTime , fcstValue from Weather_Forecast where nx = ? and ny = ? order by fcstdate , fcsttime"

# params = ( nx , ny)

# df = pd.read_sql_query(sql , con = engine , params=params)
# print(df)

# grouped = df.groupby(['fcstDate' , 'fcstTime'])

# data = []
# for idx , group in grouped:
    
#     row = {}

#     print(group['fcstDate'])
#     row['예상시간'] = f'{group['fcstDate'][0]} : {group['fcstTime'][0]}'

#     group = group.drop(['fcstDate' , 'fcstTime'], axis=1)

#     for idx , (key , value) in group.iterrows():
#         row[key] = value
    
#     data.append(row)




