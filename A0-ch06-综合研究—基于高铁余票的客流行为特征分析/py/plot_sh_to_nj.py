# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt

df_hu_ning = pd.read_csv('C:/12306data/HuNing-2016-12-21.csv',names=[u'train_no',
                                                               u'station_train_code',
                                                               u'from_station_name',
                                                               u'to_station_name',
                                                               u'start_time',
                                                               u'swz_num',
                                                               u'tz_num',
                                                               u'zy_num',
                                                               u'ze_num',
                                                               u'wz_num',
                                                               u'record_date',
                                                               u'record_time',]
                         ,encoding='utf-8')

df_SH_NJ = df_hu_ning.copy()
df_SH_NJ = df_SH_NJ[(df_SH_NJ['from_station_name'] == u'上海') & (df_SH_NJ['to_station_name'] == u'南京')]
df_SH_NJ['all_tickets'] = df_SH_NJ['swz_num'] + df_SH_NJ[u'tz_num'] +\
df_SH_NJ[u'zy_num']  + df_SH_NJ[u'ze_num'] + df_SH_NJ[u'wz_num'] 

plt.style.use('ggplot')
df_SH_NJ.plot(kind='line',y='all_tickets', x ='start_time',figsize=(14,5), legend=False,fontsize=6)
plt.xlabel(u'时 间(2016-12-21 06:00—23:00)',size=10)
plt.ylabel(u'上下客流量值（单位：人）',size=10)
plt.title(u'苏州地区站点（上海——南京）\n',size=10)
plt.tight_layout()
plt.savefig('sh_nj.png',dpi=300)
plt.show()
print('finished!')