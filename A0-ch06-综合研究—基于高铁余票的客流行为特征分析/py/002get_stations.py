# -*- coding:utf-8 -*-

import requests
import pandas as pd
import json
#import arrow
import warnings
warnings.filterwarnings("ignore")



class GetTrainNums(object):
    
    def __init__(self,from_station,to_station,date):
        self.from_station = from_station
        self.to_station = to_station
        self.date = date


    def get_train_text(self):
        # para = para
        r = requests.get('https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate='+self.date+\
            '&from_station='+self.from_station +'&to_station=' + self.to_station,
            verify=False).text
        return r

    def get_train_no(self):
        js = self.get_train_text()
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
        return df_use[u'train_no']


class GetStationNames(object):    
    def __init__(self,from_station,to_station,date,train_num,out_csv):
        self.from_station = from_station
        self.to_station = to_station
        self.date = date
        self.train_num = train_num
        self.out_csv = out_csv

    def get_stations_text(self):
        r = requests.get('https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no='+self.train_num+\
                         '&from_station_telecode='+self.from_station+\
                         '&to_station_telecode='+self.from_station+'&depart_date='+self.date,
                         verify=False).text
        return r

    def get_stations_names(self):        
        js1 = self.get_stations_text()

        js2 = json.loads(js1)
        data = js2['data']['data']
        df = pd.DataFrame(data)
        try:
            df = df[["station_name",]]
            df_use = pd.DataFrame({'train_no':[''],'station_name':['']})
            df_use['train_no'] = self.train_num
            df_use['station_name'] = df_use['station_name'].apply(lambda x: df["station_name"].values)
            
            df_use.to_csv(self.out_csv, mode = 'a',index=False,header=False,encoding='utf-8')
            print(self.train_num)
        except:
            pass



if __name__ == '__main__':
    from_station = 'SHH'
    to_station = 'NJH'
    date= '2016-12-29'
    out_csv = './data/'+from_station+'-'+to_station+'-train_names.csv'
    
    js = GetTrainNums(from_station,to_station,date)
    train_nums = js.get_train_no()
    
    for train_num in train_nums:
        stations = GetStationNames(from_station,to_station,date,train_num.strip(),out_csv)
        # js = stations.get_stations_names(train_num.strip())
        stations.get_stations_names()
    print('finished')