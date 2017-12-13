# -*- coding:utf-8 -*-

import requests
import pandas as pd
import json
import schedule
import threading
import time
import arrow
from itertools import combinations
import warnings
warnings.filterwarnings("ignore")

class HighSpeed(object):
    def __init__(self,date,from_station,to_station,direction):
        self.date = date
        self.from_station = from_station
        self.to_station = to_station
        self.direction = direction

    def get_pd(self):
        try:
	        para = 'queryDate=' + self.date + '&from_station=' + self.from_station \
	               +'&to_station=' + self.to_station
	        r = requests.get('https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&' + \
	                         para, verify=False).text
        	return r
        except:
			fl = open('./data/log.txt','a')
			fl.write('requests error at ' + str(arrow.now().format('HH:mm'))+ "\n")
			fl.close()
			print("requests error at "+str(arrow.now().format('HH:mm')))

    def to_csv(self):
        js = self.get_pd()
        try:
	        js2 = json.loads(js)
	        data = js2['data']['datas']
	        df = pd.DataFrame(data)
	        df_use = df[[u'train_no',
                         u'station_train_code',
	                     u'from_station_name',
	                     u'to_station_name',
	                     u'start_time',
	                     u'swz_num',
	                     u'tz_num',
	                     u'zy_num',
	                     u'ze_num',
	                     u'wz_num',
	                     ]]
	        df_use = df_use[df_use[u'station_train_code'].str.startswith('G') | \
	        df_use[u'station_train_code'].str.startswith('D')]
	        df_use.replace('--',0,inplace=True)
	        df_use.replace(u'无',0,inplace=True)
	        tm = arrow.now()
	        df_use['record_date'] = tm.format('YYYY-MM-DD')
	        df_use['record_time'] = tm.format('HH:mm')
	        df_use.to_csv('./data/' + self.direction + "-" +self.date + '.csv',mode = 'a', index = False, header = False,encoding='utf-8')
        except:
        	print 'no json data!'
        print 'I am working!'

    
        
if __name__ == '__main__':
       
    def process_hspeed():
        date = arrow.now().format('YYYY-MM-DD')    
        
        hu_ning = ['SHH','KNH','SZH','WXH','CZH','DYH','ZJH','NJH']
        com = combinations(hu_ning,2)
        for ls_hu_ning in com:
            hspeed = HighSpeed(date,ls_hu_ning[0],ls_hu_ning[1],'HuNing')
            hspeed.to_csv()
    
    def process_hspeed2():   
        date = arrow.now().format('YYYY-MM-DD')
        ning_hu = ['NJH','ZJH','DYH','CZH','WXH','SZH','KNH','SHH']
        com = combinations(ning_hu,2)
        for ls_ning_hu in com:
            hspeed = HighSpeed(date,ls_ning_hu[0],ls_ning_hu[1],'NingHu')
            hspeed.to_csv()

    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()


#     def job():
#         print("I'm working...")

    schedule.every(1).minutes.do(run_threaded,process_hspeed)
    schedule.every(1).minutes.do(run_threaded,process_hspeed2)
    # schedule.every().hour.do(job)
    # schedule.every().day.at("14:09").do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

