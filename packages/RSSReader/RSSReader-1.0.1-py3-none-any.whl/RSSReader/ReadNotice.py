from requests_html import HTMLSession
import json
import pymongo
import xmltodict
from dateutil import parser 
class ReadNotice(object):
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
		un_dressed=HTMLSession().get(self.__source_url)
		#print(un_dressed.text.replace("var  = ","").strip(';'))
		data= json.loads(un_dressed.text.replace("var  = ","").strip(';'))
		notice_item={}
		#mongodb connection
		myclient=pymongo.MongoClient(self.__db_url) 
		mydb=myclient[self.__db_name]
		mycollection=mydb[self.__tbl_name]
		i=0
		while(i<len(data["data"])):
			notice_item["title"] =data["data"][i]["NOTICETITLE"]
			notice_item["pubDate"]=parser.parse(data["data"][i]["NOTICEDATE"])
			notice_item["link"]=data["data"][i]["Url"]
			notice_item["description"]=data["data"][i]["ANN_RELCOLUMNS"][0]["COLUMNNAME"]
			notice_item["type"]='notice'
			exitDoc=mycollection.find_one({"title":notice_item["title"],"type":notice_item["type"]})
			if exitDoc is None:
				mycollection.insert_one(notice_item)
			notice_item.clear()
			i+=1
if __name__ == '__main__':
	ReadNotice("http://data.eastmoney.com/notices/getdata.ashx?StockCode=603713&CodeType=1&PageIndex=1&PageSize=100",
		"mongodb://47.103.117.130","rss-news","newstest").Reader()
	# NoticeReader("https://pixabay.com/images/search/美女/","div.search_results > div.nsfw > a > img").Reader()

		
