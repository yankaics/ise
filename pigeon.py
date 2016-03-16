#!/usr/bin/env python
#encoding=utf-8
import urllib2
import MySQLdb
import MySQLdb.cursors
from bs4 import BeautifulSoup
import time
from isemod import ant

host = 'csdn'
url = 'http://download.csdn.net/detail/sunnyboy9/9460441'
level = 1
deep = 3
#连接数据库
db = MySQLdb.connect(host='127.0.0.1', user='root', passwd='hong_1987', db='ise', charset='utf8', cursorclass=MySQLdb.cursors.DictCursor)
cursor = db.cursor()

#生成uniqid
def uniqid():
	ts = int(time.time() * 1000000)
	return str(hex(ts))[2:15]

#判断url唯一性
def existsHref(href):
	sql = 'select count(*) as c from t_url_list where url_src=%s'
	cursor.execute(sql, (href,))
	result = cursor.fetchone()
	return result['c']

#保存url
def saveUrl(obj):
	href = obj['href']
	if existsHref(href) == 0:
		if href[0:4] == 'http':
			title = ''
			if obj.has_key('title'):
				title = obj['title']
			content = obj.string
			if content:
				content = content.strip()
			else:
				content = ''

			sql = 'insert into t_url_list (url_id,url_src,url_title,url_content,url_ctime,url_utime,url_level)'\
				' values (%s,%s,%s,%s,%s,%s,%s)'
			cursor.execute(sql, (uniqid(), href, title, content, time.mktime(time.localtime()), 0, level))
			print 'insert url in ',level,'.'

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
	soup = BeautifulSoup(content, "html.parser")
	#解析当前html
	for s in soup.select('a'):
		s.clear()
	for s in soup.select('script'):
		s.clear()
	for s in soup.select('style'):
		s.clear()
	for s in soup.select('footer'):
		s.clear()

	content = soup.body.get_text(' ',strip=True)
	ant.build(content, 1123)
	#保存下级url
	'''
	alist = soup.select('a')
	for item in alist:
		if item.has_key('href'):
			saveUrl(item)
	'''
spider(url)
