#!/usr/bin/env python
#encoding=utf-8
import urllib2
import MySQLdb
import MySQLdb.cursors
from bs4 import BeautifulSoup
from isemod import ant
import time
import os
#主域名
host = 'csdn'
#当前爬行入口
url = 'http://www.csdn.net'
#当前页面级别
level = 1

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
def saveUrl(obj, lv):
	href = obj['href']
	#判断是否跨域
	if existsHref(href) == 0:
		if href[0:4] == 'http' and href.find(host) != -1:
			url_id = uniqid()
			sql = 'insert into t_url_list (url_id,url_src,url_ctime,url_utime,url_level)'\
				' values (%s,%s,%s,%s,%s)'
			cursor.execute(sql, (url_id, href, time.mktime(time.localtime()), 0, lv))
			print 'insert url in ',str(lv),'.'

#爬虫
def spider(uid, url, lv):
	#数据报头
	header = {}
	header['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0'
	header['Referer'] = url
	#获取页面数据
	request = urllib2.Request(url, headers=header)
	response = urllib2.urlopen(request)
	result = response.read()
	#保存快照
	'''
	with open('cache/' + uid + '.html', 'w') as f:
		f.write(result)
	'''
	#解析html文档
	parseHtml(uid, result, lv)


#html解析器
def parseHtml(uid, content, lv):
	soup = BeautifulSoup(content, "html.parser")
	#保存下级url
	alist = soup.select('a')
	for item in alist:
		if item.has_attr('href'):
			saveUrl(item, lv)
		item.clear()
	#获取内容进行分词
	'''
	for s in soup.select('script'):
		s.clear()
	for s in soup.select('style'):
		s.clear()
	for s in soup.select('footer'):
		s.clear()
	content = soup.body.get_text(' ',strip=True)
	ant.build(content, uid)
	'''
#深度爬取
def deepSearch(lv):
	sql = 'select url_id,url_src from t_url_list where url_level=%s'
	cursor.execute(sql, (lv,))
	result = cursor.fetchall()
	for item in result:
		spider(item['url_id'], item['url_src'], lv+1)

#爬行入口	
spider('000', url, level)
#深度1
deepSearch(level)
#深度2
#deepSearch(level+1)
#深度3
#deepSearch(level+2)

