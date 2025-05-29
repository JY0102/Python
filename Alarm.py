
from DataBases.UpdateDB import Run

from datetime import datetime
import schedule
import time

hour = int(datetime.now().strftime("%H"))
hour_list = [2 ,5, 8, 11, 14, 17, 20, 23,]

for h in hour_list:
    if hour < h:
        hour = h
        break


def Update():
    global hour
    if hour == 23:
        hour = 2
    else :
        hour += 3
    
    print(f"데이터베이스 최신화 {datetime.now().strftime("%H%M")}")
    schedule.clear()
    schedule.every().day.at(f"{hour:02}:10").do(Update)

    Run()
    
    print(f"데이터베이스 끝 {datetime.now().strftime("%H%M")}")

schedule.every().day.at(f"{hour:02}:10").do(Update)

def worker():
    Update()

    print(hour)
    while True:
        schedule.run_pending()
        time.sleep(60)


