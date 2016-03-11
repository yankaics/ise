#!/usr/bin/env python
#encoding=utf-8
import urllib2
import MySQLdb
import MySQLdb.cursors
from bs4 import BeautifulSoup

host = 'csdn'
url = 'http://www.csdn.net'

#连接数据库
db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='hong_1987', db='ise', charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()

#保存url
def saveUrl(obj):
	href = obj['href']
	if href[0:4] == 'http':
		title = ''
		if obj.has_key('title'):
			title = obj['title']
		content = obj.string
		if content:
			content = content.strip()

		print href,title,content,"\n"


#爬虫
def spider(url):
	#数据报头
	header = {}
	header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0'
	header['Referer'] = url
	#获取页面数据
	request = urllib2.Request(url, headers=header)
	response = urllib2.urlopen(request)
	result = response.read()
	#解析html文档
	parseHtml(result)

#html解析器
def parseHtml(content):
	soup = BeautifulSoup(content)
	alist = soup.select('a')
	
	for item in alist:
		if item.has_key('href'):
			saveUrl(item)


spider(url)
