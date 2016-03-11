#!/usr/bin/env python
#encoding=utf-8
import urllib2
from bs4 import BeautifulSoup

host = 'csdn'
url = 'http://www.csdn.net'

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

def parseHtml(content):
	soup = BeautifulSoup(content)
	alist = soup.select('a')
	
	for item in alist:
		if item.has_key('href'):
			print item['href']


spider(url)
