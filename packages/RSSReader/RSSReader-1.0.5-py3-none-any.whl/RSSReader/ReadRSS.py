#url=http://news.stockstar.com/rss/xml.aspx?file=xml/stock/10.xml
# -*- coding: UTF-8 -*-
import requests
import codecs
import pymongo
import xmltodict
from dateutil import parser 
class ReadRSS:
	def __init__(self,source_url,db_url,db_name,tbl_name):
		#set default
		self.__source_url=''
		self.__db_url=''
		self.__db_name=''
		self.__tbl_name=''
		#get local
		if source_url is not None and len(source_url)>0:
			self.__source_url=source_url
		if db_url is not None and len(db_url)>0:
			self.__db_url=db_url
		if db_name is not None and len(db_name)>0:
			self.__db_name=db_name
		if tbl_name is not None and len(tbl_name)>0:
			self.__tbl_name=tbl_name
	def Reader(self):
		item_json=''
		mycollection=''
		try:
			#url = 'http://news.stockstar.com/rss/xml.aspx?file=xml/stock/10.xml'#'http://news.qq.com/newsgj/rss_newswj.xml'
			headers = {
			    'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'}
			page = requests.get(self.__source_url, headers=headers)
			page.encoding = 'utf-8'
			page_content = page.text
			#xml to json
			page_json=xmltodict.parse(page_content)
			#mongodb connection
			myclient=pymongo.MongoClient(self.__db_url) 
			mydb=myclient[self.__db_name]
			mycollection=mydb[self.__tbl_name]
			item_json=page_json["rss"]["channel"]["item"]
		except Exception as e:
			print("异常:%s获取失败"%self.__source_url)
		if(item_json is not None):
			for item in item_json:
				exitDoc=mycollection.find_one({"title":item["title"],"type":'RSS'})
				if exitDoc is None:
					#转为日期类型
					item["pubDate"] = parser.parse(item["pubDate"])
					#增加数据类型区分
					item["type"]='RSS'
					mycollection.insert_one(item)
			# 存入文件
			# f = codecs.open('d:/news.txt', 'w', 'utf-8')
			# f.write(page_content)
			#print (page_json)
			# f.close()
if __name__ == '__main__':
	#http://news.stockstar.com/rss/xml.aspx?file=xml/stock/10.xml
	ReadRSS('http://news.qq.com/newsgj/rss_newswj.xml',"mongodb://47.103.117.130","rss-news","newstest").Reader()



