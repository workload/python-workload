# -*- coding:utf-8 -*-

import requests
import pandas as pd
import json
#import arrow
import warnings
warnings.filterwarnings("ignore")

def get_pd():
    para = para
    r = requests.get('https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate=2016-12-29&from_station=SHH&to_station=NJH',
        verify=False).text
    return r

def to_csv(js):
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
#     tm = arrow.now().format('HH:mm:ss')
#     df_use['record_time'] = tm
    # df_use[u'train_no'].to_csv('./data/SH-NJ-train_no.csv',index=False,encoding='utf-8')
#     df_use[u'train_no'].to_csv('./dareta/NJ-SH-train_no.csv',index=False,encoding='utf-8')
    return df_use[u'train_no']






if __name__ == '__main__':
    # para = 'queryDate=2016-12-29&from_station=/SHH&to_station=NJH'
#     para = 'queryDate=2016-12-29&from_station=NJH&to_station=SHH'
    js = get_pd(para)
    train_no = to_csv(js)
    # print('finished')