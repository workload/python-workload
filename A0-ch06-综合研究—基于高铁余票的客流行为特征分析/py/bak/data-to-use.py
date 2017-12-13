# -*- coding:utf-8 -*-
import pandas as pd
import arrow



def data_to_use(orgdata):
# 导入数据
df_hu_ning = pd.read_csv(orgdata,encoding='utf-8')
df_hu_ning.columns = [u'train_no',u'station_train_code', u'from_station_name',u'to_station_name',
                    u'start_time',
                    u'swz_num',
                    u'tz_num',
                    u'zy_num',
                    u'ze_num',
                    u'wz_num',
              		u'record_date',
              		u'record_time',]

#筛选出发车时间在06:00-23:00的车次
df_hu_ning2 = df_hu_ning[(df_hu_ning['start_time'].str.contains("0[6-9]:|1[0-9]:|2[0-3]:"))]

#增加一列，记录发车前30分钟数据
df_hu_ning2['start_time_before30m'] = df_hu_ning2['start_time'].apply(lambda x: arrow.get(x, 'HH:mm').replace(minutes=-30).format('HH:mm'))

#筛选出：发车前30分钟时间==记录时间
df_hu_ning3 = df_hu_ning2[df_hu_ning2['start_time_before30m'] == df_hu_ning2['record_time']]

#增加一列，记录出发站，到达站数据
df_hu_ning3['from_to'] = np.nan
df_hu_ning3['from_to'] = df_hu_ning3['from_station_name'] + ',' +df_hu_ning3['to_station_name']
df_hu_ning3['from_to'] = df_hu_ning3['from_to'].str.split(',')


# df_hu_ning3为最终筛选数据
############################

#获取各车次区间情况
df_SH_NJ = pd.read_csv('./data/SH-NJ-station.csv',encoding='utf-8')
df_SH_NJ.columns=['station_name','train_no']
df_SH_NJ['station_name'] = df_SH_NJ['station_name'].apply(lambda x: x.replace(u'[',u'').replace(u']',u'').replace(' ','').split(','))
df_SH_NJ['station_interval'] = df_SH_NJ['station_name'].apply(lambda x: list(map(list, zip(x[:-1], x[1:]))))

# df_SH_NJ是沪宁所有车次相邻站点信息。

df_tickets_com = pd.merge(df_hu_ning3,df_SH_NJ,on='train_no')
df_tickets_com[df_tickets_com['train_no']=='5l000G192400'].head(2)

df_tickets_com2 = df_tickets_com[df_tickets_com.apply(lambda x: x['from_to'] in x['station_interval'], axis=1)]

