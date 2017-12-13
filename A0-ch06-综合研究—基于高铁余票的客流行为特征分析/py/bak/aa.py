# -*- coding:utf-8 -*-
import pandas as pd
import arrow
import matplotlib.pyplot as plt



class DataPlot(object):
	def __init__(self,orginal_data,orginal_station,station_to_plot):
		self.orginal_data = orginal_data
		self.orginal_station = orginal_station
		self.station_to_plot = station_to_plot
		# self.orginal_data = orginal_data

	def data_to_use(orgdata):
	# 导入数据
		df = pd.read_csv(orgdata,encoding='utf-8')
		df.columns = [u'train_no',u'station_train_code', u'from_station_name',u'to_station_name',
		                    u'start_time',
		                    u'swz_num',
		                    u'tz_num',
		                    u'zy_num',
		                    u'ze_num',
		                    u'wz_num',
		              		u'record_date',
		              		u'record_time',]

		#筛选出发车时间在06:00-23:00的车次
		df2 = df[(df['start_time'].str.contains("0[6-9]:|1[0-9]:|2[0-3]:"))]

		#增加一列，记录发车前30分钟数据
		df2['start_time_before30m'] = df2['start_time'].apply(lambda x: arrow.get(x, 'HH:mm').replace(minutes=-30).format('HH:mm'))

		#筛选出：发车前30分钟时间==记录时间
		df3 = df2[df2['start_time_before30m'] == df2['record_time']]

		#增加一列，记录出发站，到达站数据
		df3['from_to'] = np.nan
		df3['from_to'] = df3['from_station_name'] + ',' +df3['to_station_name']
		df3['from_to'] = df3['from_to'].str.split(',')
		return df3

		# df_hu_ning3为最终筛选数据
		############################

	def get_stations(orgdata):
		#获取各车次区间情况
		data_to_use = data_to_use()
		df = pd.read_csv(orgdata,encoding='utf-8')
		df.columns=['station_name','train_no']
		df['station_name'] = df['station_name'].apply(lambda x: x.replace(u'[',u'').replace(u']',u'').replace(' ','').split(','))
		df['station_interval'] = df['station_name'].apply(lambda x: list(map(list, zip(x[:-1], x[1:]))))

		# df_SH_NJ是沪宁所有车次相邻站点信息。

		df_tickets_com = pd.merge(df_hu_ning3,df_SH_NJ,on='train_no')
		df_tickets_com2 = df_tickets_com[df_tickets_com.apply(lambda x: x['from_to'] in x['station_interval'], axis=1)]
		return df_tickets_com2


	def main(cityls):
		df_to_suzhou = dff[dff['to_station_name'].isin([u'苏州',u'苏州北',u'苏州园区',u'苏州新区'])]
		df_from_suzhou = dff[dff['from_station_name'].isin([u'苏州',u'苏州北',u'苏州园区',u'苏州新区'])]
		
		df_to_suzhou['tickets_sum_to'] = df_to_suzhou['swz_num']+\
		df_to_suzhou['tz_num']+df_to_suzhou['wz_num']+df_to_suzhou['ze_num']+\
		df_to_suzhou['zy_num']

		df_from_suzhou['tickets_sum_from'] = df_from_suzhou['swz_num']+\
		df_from_suzhou['tz_num']+df_from_suzhou['wz_num']+df_from_suzhou['ze_num']+\
		df_from_suzhou['zy_num']

		suzhou_df = pd.merge(df_to_suzhou,df_from_suzhou, on = 'train_no')
		suzhou_df['tickets'] = suzhou_df['tickets_sum_to'] - suzhou_df['tickets_sum_from']

		suzhou_df['start_time_y'] = suzhou_df['start_time_y'].\
		apply(lambda x: arrow.get(str(x),'YY-MM-DD HH:mm:ss').format('HH:mm'))
		
		suzhou_df_to_plot = suzhou_df[['tickets','start_time_y','train_no','station_train_code_x','station_train_code_y']]
		return suzhou_df_to_plot

if __name__ == '__main__':
	plot_data = main()
	plt.style.use('ggplot')

	dmt= suzhou_df_to_plot2.sort_values(by='start_time_y')
	dmt.plot(y='tickets', x ='start_time_y',kind = 'bar',figsize=(14,5), legend=False,fontsize=6)
	plt.xlabel(u'时 间(2016-12-21 06:00—23:00)',size=10)
	plt.ylabel(u'上下客流量值（单位：人）',size=10)
	plt.title(u'苏州地区站点（上海——南京）\n',size=10)
	# plt.show()
	# plt.tight_layout()
	plt.savefig('suzhou.png',dpi=300)