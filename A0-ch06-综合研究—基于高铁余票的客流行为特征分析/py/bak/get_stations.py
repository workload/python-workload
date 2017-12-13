import requests
import pandas as pd
import json
#import arrow
import warnings
warnings.filterwarnings("ignore")


def get_pd(para):
    para = para
    r = requests.get('https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no='+para+\
                     '&from_station_telecode=NJH&to_station_telecode=SHH&depart_date=2016-12-29',
                     verify=False).text
    return r

def to_csv(para,js):
    js2 = json.loads(js)
    data = js2['data']['data']
    df = pd.DataFrame(data)
    try:
        df = df[["station_name",]]
        df_use = pd.DataFrame({'train_no':[''],'station_name':['']})
        df_use['train_no'] = para.strip()
        df_use['station_name'] = df_use['station_name'].apply(lambda x: df["station_name"].values)
    #     df_use['start_time'] = df_use['start_time'].apply(lambda x: df["start_time"].values)
    #     df_use = df_use[df_use[u'station_train_code'].str.startswith('G') | \
    #     df_use[u'station_train_code'].str.startswith('D')]
    #     df_use.replace('--',0,inplace=True)
    #     df_use.replace(u'无',0,inplace=True)
    #     tm = arrow.now().format('HH:mm:ss')
    #     df_use['record_time'] = tm
        df_use.to_csv('./data/NJ-SH-station.csv',mode = 'a',index=False,header=False,encoding='utf-8')
    except:
        pass
if __name__ == '__main__':
#     para = '55000G707270'
#     js = get_pd(para)
#     to_csv(para,js)
#     print('finished')
    station_no_file = open('./data/NJ-SH-train_no.csv','r')
    station_no_data = station_no_file.readlines()
    for station_no in station_no_data:
#         print station_no.strip()
#         para = '55000G707270'
        js = get_pd(station_no.strip())
        to_csv(station_no.strip(),js)
    print('finished')