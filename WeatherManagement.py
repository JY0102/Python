
from OpenApi import Api
from datetime import datetime
from DataBase import DB

class Weather:
    
    db = DB()

    # 검색기능
    def Search(self , step1 , step2):   
        nx,ny = self.db.SelectRegion(step1 , step2)
        api_data = Api.Search(nx,ny)
        
        if not api_data: return        

        data = []
        row = {}

        for (name1 , name2 ), group in api_data:
            row.clear()

            row['예상시간'] = f'{name1} : {name2}'

            for idx, data in group.iterrows():
                key , value = self.CodeToString(data)
                row[key] = value
            
            data.append(row)
        
        return (step1 , step2) , data

    
        # 출력 디버깅용
        # print(f'현재 시각 ({datetime.now().strftime('%Y%m%d')} / {datetime.now().strftime('%H00')} )')
        # print(f'[{step1} {step2} 날씨 현황 ]')

        # for (name1 ,name2), group in api_data:
        #     print('\n\n')

        #     print(group)
        #     print(f'예상시각 : {name1} : {name2}')
        #     for idx , data in group.iterrows():
        #        self.PrintInfo(data)


    def CodeToString(self , data):        
        name , unit = self.db.SelectCategory( '단기예보' , data['category'] )

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

            if data['fcstValue'] == '강수없음':
                unit = '강수없음'
            elif data['fcstValue'] == '적설없음':
                unit = '적설없음'

            return name , unit
        else :
            return name , f'{data['fcstValue']} {unit}'

    # def PrintInfo(self , data):        
    #     name , unit = self.db.SelectCategory( '단기예보' , data['category'] )

    #     if unit == '코드값':
    #         if name == '하늘상태':
    #             match data['fcstValue']:
    #                 case '1': unit = '맑음'
    #                 case '3': unit = '구름 많음'
    #                 case '4': unit = '흐림'
    #         elif name == '강수형태':
    #             match data['fcstValue']:
    #                 case '0': unit = '없음'
    #                 case '1': unit = '비'
    #                 case '2': unit = '비/눈'
    #                 case '3': unit = '눈'
    #                 case '4': unit = '소나기'

    #         print(f'{name } : {unit}')
    #     elif data['fcstValue'] == '강수없음':
    #         unit = '강수없음'
    #         print(f'{name } : {unit}')
    #     elif data['fcstValue'] == '적설없음':
    #         unit = '적설없음'
    #         print(f'{name } : {unit}')
    #     else :
    #         print(f'{name } : {data['fcstValue']}{unit}')