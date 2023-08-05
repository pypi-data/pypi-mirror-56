# 使用年月日 定时
from datetime import *
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import RSSReader
import configparser
import os

import requests
import codecs
import pymongo
import xmltodict
class BatchRSS(object):
	def __init__(self,**param):
		def Run():
			print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
			#读取配置文件抓数据
			conf=configparser.ConfigParser()
			conf.read("RSSReader.ini",encoding='utf-8')
			db_url,db_name,tbl_name=None,None,None
			if conf.has_option("mongodb","db_url"):
				db_url=conf.get("mongodb","db_url")
			if conf.has_option("mongodb","db_name"):
				db_name=conf.get("mongodb","db_name")
			if conf.has_option("mongodb","tbl_name"):				
				tbl_name=conf.get("mongodb","tbl_name")
			for section in conf.sections():
				base_url=""
				url_items=""
				if conf.has_option(section,"base_url"):
					base_url=conf.get(section,"base_url")
				if conf.has_option(section,"url"):
					url=conf.get(section,"url")
					url_items=filter(None,url.split(" "))
					for url_item in url_items:
						print("抓取:"+base_url+url_item)
						try:
							RSSReader.RSSReader(base_url+url_item,db_url,db_name,tbl_name).Reader()
						except Exception as e:
							print(e)
			print("执行结束")
		sched = BlockingScheduler()
		sched.add_job(func=Run,**param)
		#sched.add_job(func=Run,args=('循环任务',),trigger='date',run_date="2019-11-15 16:15:59")
		sched.start()
if __name__ == '__main__':
	batchRun=BatchRSS(trigger='interval',seconds=10)
