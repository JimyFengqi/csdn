# -*- coding: utf-8 -*-
# @Date    : 2018-08-20 13:48:04
# @Author  : Jimy_Fengqi (jmps515@163.com)
# @Link    : https://blog.csdn.net/qiqiyingse/
# @Version : v1.0

import os
import sys
import time 
import random

import json
import re
import requests
from pyquery import PyQuery as pq

import xlrd
import xlwt
from xlwt import Workbook
from xlutils.copy import copy
from functools import cmp_to_key

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pymongo

class PymongoDataSave():
	def __init__(self,data='test'):
		self.client=pymongo.MongoClient()
		self.csdn=self.client.CSDN     #数据库的db名字
		self.dbtable=self.csdn['qiqiyingse']   #table名字
		if data=='test':
			logger('no New data need handle, just querry')
			self.print_database_and_table_name()
			
		else:
			logger('New data need handle')
			self.data=data
			self.handleData()
	#抽取所有关键字段，组成列表		
	def getURLlistdata(self,keyElement='文章地址'):
		return self.dbtable.distinct(keyElement)

	#查询一个table里面某个字段的数量
	def findDataNumInDB(self,keyElement='阅读数'):	
		num=self.dbtable.find({keyElement:{'$exists':True}}).count() #整个字段是否存在,返回个数
		logger('current data element [%s] has Num :[%d]'%(keyElement,num))

		
	def saveDataInDB(self,datalist,qurryElement='文章地址',compareElement='阅读数',ranknum='排行'):
		#self.dbtable.find({compareElement:{'$exists':True}}).count() #整个字段是否存在,返回个数
		#self.dbtable.find({compareElement:None}).count() #字段是否存在
		#self.dbtable.distinct('articles_url')  #获取这个字段，将所有这个的内容组成列表返回
		for single_data in datalist:
			tmp=single_data[qurryElement]
			tmp_element=self.dbtable.find_one({qurryElement:tmp})
			tmp_count=self.dbtable.find({qurryElement:tmp}).count()

			if tmp_count>1:
				logger('current info exist num is[%d] , need to do a remove, [element]%s ' % tmp_count,tmp_element)#当前数量大于1，做一次删除
				self.dbtable.remove({qurryElement:tmp},0)
			elif tmp_count == 1:
				old_read_num=tmp_element[compareElement]
				current_read_num=single_data[compareElement]

				if current_read_num>old_read_num:
					#这种是直接更新，并且追加新元素，它是没有破环新的元素，直接更新了数据库， 
					#最终，如果数据一直更新，数据库中的数据和新的数据相比多了一个元素，如果一直不更新
					self.dbtable.update({qurryElement:tmp},{'$set':{'之前阅读数':old_read_num,compareElement:current_read_num}})
					
					'''
					#这种是先将数据增加新元素，然后删除数据库中已经存在的一个数据，再将新数据插入，原有数据已经被破坏
	
					single_data['old_read_num']=old_read_num
					self.dbtable.remove({qurryElement:tmp},0)  #删除存在的老数据
					self.dbtable.insert_one(single_data)
					'''

				old_rank=tmp_element[ranknum]
				current_rank=single_data[ranknum]
				if current_rank!=old_rank:
					self.dbtable.update({qurryElement:tmp},{'$set':{'之前排行':old_rank,ranknum:current_rank}})

			else:
				self.dbtable.insert_one(single_data)

	#插入数据之前，遍历一下整个数据库			
	def handleData(self):
		self.print_database_and_table_name()
		self.saveDataInDB(self.data)
		
	def print_database_and_table_name(self):
		logger(self.client.database_names())#获取打印所有的db名字
		#遍历每一个db,打印每一个table
		for database in self.client.database_names():
			for table in self.client[database].collection_names():
				logger('table [%s] 有 [%d]个数据，属于 database [%s]' %(table,self.client[database][table].find().count(),database))

#自定义log函数，主要是加上时间
def logger(msg):
		print ('%s: %s' % (time.strftime('%Y-%m-%d_%H-%M-%S'), msg))

class CSDNSpider():
	def __init__(self):
		#自己博客主页
		#self.csdn_url = 'http://blog.csdn.net/qiqiyingse?viewmode=contents'
		self.csdn_url = 'https://blog.csdn.net/qiqiyingse/article/list/4?orderby=ViewCount'
		self.page_base_url="http://blog.csdn.net/qiqiyingse/article/list/"
		self.contentList=[]
		self.contentLists=[]
								
		# 爬虫伪装头部设置
		self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
		
		# 设置操作超时时长
		self.timeout = 5
		
		# 爬虫模拟在一个request.session中完成
		self.mySession = requests.Session()

		self.phantomjs_path=r'C:\code\phantomjs-2.1.1-windows\bin\phantomjs.exe'
		self.chromedriver_path=	r'C:\code\phantoPmjs-2.1.1-windows\bin\chromedriver.exe'

		self.mylisttest=[{'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/81980458', 'acticle_title': '转 python 获取操作系统信息或者用户名', 'read_num': 20, 'index': 1}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/81776735', 'acticle_title': '原 NodeJS学习（2）构建第一个爬虫', 'read_num': 49, 'index': 2}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/81668517', 'acticle_title': '转 Python Webdriver 重新使用已经打开的浏览器实例', 'read_num': 55, 'index': 3}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/81281658', 'acticle_title': '原 python 小工具--像打字机一样输出内容', 'read_num': 55, 'index': 4}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/81567080', 'acticle_title': '原 python实现屏幕录制', 'read_num': 64, 'index': 5}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/81565263', 'acticle_title': '转 解决Python读取文件时出现编码异常', 'read_num': 67, 'index': 6}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/79442645', 'acticle_title': '转 安装scrapy报错 Python.h: 没有那个文件或目录', 'read_num': 97, 'index': 7}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/80269610', 'acticle_title': '原 Android 编译,烧机的一些方法', 'read_num': 108, 'index': 8}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/81668345', 'acticle_title': '原 python实现实时电脑监控', 'read_num': 113, 'index': 9}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/79473830', 'acticle_title': '转 GitHub上README.md教程', 'read_num': 121, 'index': 10}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/78141474', 'acticle_title': '转 设计模式（七）策略模式详解', 'read_num': 189, 'index': 11}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/78141487', 'acticle_title': '转 设计模式（八）适配器模式详解', 'read_num': 210, 'index': 12}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/79471056', 'acticle_title': '原 使用 Python时常用的安装包', 'read_num': 221, 'index': 13}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/77855473', 'acticle_title': '原 python实现的一种排序方法', 'read_num': 221, 'index': 14}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/79471634', 'acticle_title': '转 微信小程序集合', 'read_num': 249, 'index': 15}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71543110', 'acticle_title': '原 Mongodb学习（2）概念学习——ACID原则', 'read_num': 365, 'index': 16}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/74004388', 'acticle_title': '转 设计模式（五）抽象工厂模式详解', 'read_num': 367, 'index': 17}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72540866', 'acticle_title': '原 python学习——邮件发送程序', 'read_num': 370, 'index': 18}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/78210646', 'acticle_title': '原 python 实现文件查找功能', 'read_num': 400, 'index': 19}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71544282', 'acticle_title': '原 Mongodb学习（2）概念学习——基本内容', 'read_num': 411, 'index': 20}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72961382', 'acticle_title': '原 redis学习（1）python连接redis', 'read_num': 454, 'index': 21}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72453537', 'acticle_title': '原 Mongodb学习（5）pymongdb的使用', 'read_num': 471, 'index': 22}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71643828', 'acticle_title': '原 Python挑战游戏汇总', 'read_num': 485, 'index': 23}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/78132072', 'acticle_title': '转 用Python实现一个简单的文件传输协议', 'read_num': 486, 'index': 24}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71647261', 'acticle_title': '原 Python挑战游戏( PythonChallenge)闯关之路Level 0', 'read_num': 490, 'index': 25}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/77747777', 'acticle_title': '转 python数据持久存储：pickle模块的基本使用', 'read_num': 507, 'index': 26}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/77835705', 'acticle_title': '原 Mongodb学习（10）一个小例子', 'read_num': 520, 'index': 27}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72566001', 'acticle_title': '原 Mongodb学习（6）pymongdb的数据库的拷贝', 'read_num': 542, 'index': 28}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72898831', 'acticle_title': '原 Node.js学习（1）牛刀小试', 'read_num': 568, 'index': 29}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/77745548', 'acticle_title': '原 Python挑战游戏( PythonChallenge)闯关之路Level- 5', 'read_num': 572, 'index': 30}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72558839', 'acticle_title': '原 pythonUI学习实践（1）制作自己的闹钟', 'read_num': 575, 'index': 31}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71514942', 'acticle_title': '原 Mongodb学习（1）安装以及配置', 'read_num': 577, 'index': 32}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71757964', 'acticle_title': '原 Python挑战游戏( PythonChallenge)闯关之路Level- 3', 'read_num': 598, 'index': 33}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/74004472', 'acticle_title': '转 设计模式（六）观察者模式详解（包含观察者模式JDK的漏洞以及事件驱动模型）', 'read_num': 609, 'index': 34}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71580496', 'acticle_title': '转 设计模式（四）工厂方法模式详解（另附简单工厂的死亡之路）', 'read_num': 614, 'index': 35}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71756381', 'acticle_title': '原 python练习题——string模块', 'read_num': 622, 'index': 36}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72953832', 'acticle_title': '原 Mongodb学习（9）集群搭建以及错误处理', 'read_num': 637, 'index': 37}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72633533', 'acticle_title': '原 Mongodb学习（7）pymongdb的使用——打印数据库名和table名', 'read_num': 734, 'index': 38}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71226818', 'acticle_title': '转 设计模式详解（总纲）', 'read_num': 777, 'index': 39}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71747671', 'acticle_title': '原 Python挑战游戏( PythonChallenge)闯关之路Level- 2', 'read_num': 835, 'index': 40}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71547716', 'acticle_title': '原 Mongodb学习（3）基本操作——增删改查', 'read_num': 855, 'index': 41}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71678011', 'acticle_title': '原 Python挑战游戏( PythonChallenge)闯关之路Level- 1', 'read_num': 859, 'index': 42}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/78225394', 'acticle_title': '原 Python 实现替换文件里面的内容', 'read_num': 898, 'index': 43}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/77749109', 'acticle_title': '原 Python挑战游戏( PythonChallenge)闯关之路Level- 6', 'read_num': 926, 'index': 44}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71232015', 'acticle_title': '原 使用python一键登录博客', 'read_num': 1033, 'index': 45}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72553276', 'acticle_title': '转 Python图像处理库PIL的ImageFilter模块介绍', 'read_num': 1072, 'index': 46}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71216102', 'acticle_title': '原 python excel使用进阶篇', 'read_num': 1128, 'index': 47}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/79487514', 'acticle_title': '原 linux环境 安装chromedriver 和 phantomjs的方法', 'read_num': 1179, 'index': 48}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72285927', 'acticle_title': '原 Python挑战游戏( PythonChallenge)闯关之路Level- 4', 'read_num': 1251, 'index': 49}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71405436', 'acticle_title': '转 python 的日志logging模块学习', 'read_num': 1323, 'index': 50}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71218711', 'acticle_title': '原 在python上使用wordcloud制作自己的词云', 'read_num': 1515, 'index': 51}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71172347', 'acticle_title': '原 使用python装饰器计算函数运行时间', 'read_num': 1519, 'index': 52}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72553279', 'acticle_title': '原 python技巧——自己做验证码', 'read_num': 1525, 'index': 53}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71123322', 'acticle_title': '转 Python下调用Linux的Shell命令', 'read_num': 2118, 'index': 54}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/78501034', 'acticle_title': '原 python爬虫（19）爬取论坛网站——网络上常见的gif动态图', 'read_num': 2199, 'index': 55}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/72633711', 'acticle_title': '原 Mongodb学习（8）pymongdb的使用——数据去重', 'read_num': 2584, 'index': 56}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71640203', 'acticle_title': '原 python爬虫（10）身边的翻译专家——获取有道翻译结果', 'read_num': 2600, 'index': 57}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59483706', 'acticle_title': '原 08_python_练习题——乘法表', 'read_num': 2912, 'index': 58}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59488018', 'acticle_title': '原 python——利用python通过浏览器打开博客页面', 'read_num': 2987, 'index': 59}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71227451', 'acticle_title': '转 （一）单例模式详解', 'read_num': 2994, 'index': 60}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70048820', 'acticle_title': '转 Python中PyQuery库的使用总结', 'read_num': 3007, 'index': 61}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71122905', 'acticle_title': '原 python小工具——下载更新代码工具', 'read_num': 3035, 'index': 62}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59112217', 'acticle_title': '原 01_python_练习题_使用python直接打开网页', 'read_num': 3053, 'index': 63}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59483629', 'acticle_title': '原 07_python_练习题——数值排序', 'read_num': 3063, 'index': 64}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70143777', 'acticle_title': '原 17_python_练习题——打印指定目录下的文件和文件夹（相当于tree命令）', 'read_num': 3078, 'index': 65}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60132246', 'acticle_title': '转 [Python] xrange和range的使用区别', 'read_num': 3090, 'index': 66}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60144027', 'acticle_title': '原 13_python_练习题——文件重定向', 'read_num': 3098, 'index': 67}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/67641261', 'acticle_title': '原 12_python爬虫——下载个人CSDN博客内容', 'read_num': 3102, 'index': 68}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59112479', 'acticle_title': '原 02_python_练习题——图形界面', 'read_num': 3142, 'index': 69}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60582816', 'acticle_title': '原 python爬虫（5）黑板客第三关', 'read_num': 3168, 'index': 70}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59481693', 'acticle_title': '原 05_python_练习题——平方数', 'read_num': 3169, 'index': 71}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60129630', 'acticle_title': '原 12_python_练习题——统计输入字符里面有多少', 'read_num': 3209, 'index': 72}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/55260352', 'acticle_title': '原 Python的安装', 'read_num': 3213, 'index': 73}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/55517278', 'acticle_title': '转 python version 2.7 required,which was not found in the registry', 'read_num': 3274, 'index': 74}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62427733', 'acticle_title': '原 15_python_练习题——使用webdriver查询IP地址', 'read_num': 3290, 'index': 75}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60582751', 'acticle_title': '原 15_python_练习题——打印日历', 'read_num': 3329, 'index': 76}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/61197123', 'acticle_title': '原 统计个人CSDN的博客文章数量', 'read_num': 3340, 'index': 77}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60572338', 'acticle_title': '原 python爬虫（4）四种方法通过黑板客第二关', 'read_num': 3350, 'index': 78}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70208940', 'acticle_title': '原 19_python_练习题——CSV文件读写练习', 'read_num': 3375, 'index': 79}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70172218', 'acticle_title': '原 18_python_练习题——写入文件到word文档中', 'read_num': 3378, 'index': 80}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/64522690', 'acticle_title': '原 python爬虫（7）爬取糗事百科段子（UI版）', 'read_num': 3378, 'index': 81}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70125444', 'acticle_title': '转 linux后台运行和关闭、查看后台任务', 'read_num': 3406, 'index': 82}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70145804', 'acticle_title': '转 SSH 的详细使用方法', 'read_num': 3434, 'index': 83}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70855457', 'acticle_title': '转 python的一个好玩模块wordcloud', 'read_num': 3438, 'index': 84}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70843626', 'acticle_title': '转 shell脚本：Syntax error: Bad for loop variable错误解决方法', 'read_num': 3439, 'index': 85}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/55259304', 'acticle_title': '原 py2exe的使用', 'read_num': 3487, 'index': 86}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70161637', 'acticle_title': '转 卸载win10 自带应用', 'read_num': 3514, 'index': 87}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/68926007', 'acticle_title': '原 python——一个投票器', 'read_num': 3514, 'index': 88}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59113090', 'acticle_title': '原 04_python_练习题——企业利润', 'read_num': 3533, 'index': 89}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70138912', 'acticle_title': '转 Python爬虫防封杀方法集合', 'read_num': 3639, 'index': 90}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60144578', 'acticle_title': '原 python爬虫（3）五种方法通过黑板客第一关', 'read_num': 3826, 'index': 91}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71131120', 'acticle_title': '原 将python代码和注释分离', 'read_num': 3998, 'index': 92}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71308389', 'acticle_title': '转 （二）代理模式详解（包含原理详解）', 'read_num': 4186, 'index': 93}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71344110', 'acticle_title': '转 （三）简单工厂模式详解', 'read_num': 4198, 'index': 94}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62427155', 'acticle_title': '原 python爬虫(14)获取淘宝MM个人信息及照片（上）', 'read_num': 4217, 'index': 95}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62896264', 'acticle_title': '原 16_python_练习题——使用webdriver获取当前页面截屏以及滑动页面', 'read_num': 4311, 'index': 96}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/69944173', 'acticle_title': '原 将自己的python程序打包成exe', 'read_num': 4478, 'index': 97}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71616418', 'acticle_title': '原 Mongodb学习（4）通过配置文件启动mongod', 'read_num': 4503, 'index': 98}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/46800751', 'acticle_title': '原 几行代码解决大端小端的问题', 'read_num': 4725, 'index': 99}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60583419', 'acticle_title': '原 14_python_练习题——excel操作', 'read_num': 4890, 'index': 100}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70046543', 'acticle_title': '原 quote函数什么意思，怎么用', 'read_num': 4936, 'index': 101}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71123348', 'acticle_title': '转 黄聪：Python 字符串操作（string替换、删除、截取、复制、连接、比较、查找、包含、大小写转换、分割等 ）', 'read_num': 4957, 'index': 102}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62236845', 'acticle_title': '原 python爬虫(12)获取七天内的天气', 'read_num': 5102, 'index': 103}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59526995', 'acticle_title': '原 11_python_练习题——日期格式显示', 'read_num': 5301, 'index': 104}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70855068', 'acticle_title': '转 抓取网易云音乐歌曲 热门评论生成词云（转）', 'read_num': 5312, 'index': 105}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71325615', 'acticle_title': '原 python_随机调用一个浏览器打开网页', 'read_num': 5543, 'index': 106}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70049591', 'acticle_title': '原 json.dumps和 json.loads 区别，如此简单', 'read_num': 5649, 'index': 107}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59502402', 'acticle_title': '原 10_python_练习题——兔子问题与斐波那契數列', 'read_num': 5831, 'index': 108}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59483966', 'acticle_title': '原 09_python_练习题——暂停一秒', 'read_num': 5879, 'index': 109}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59483536', 'acticle_title': '原 06_python_练习题——查找一年之中第几天', 'read_num': 5930, 'index': 110}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/59112715', 'acticle_title': '原 03_python_练习题——排列组合', 'read_num': 5949, 'index': 111}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62231679', 'acticle_title': '原 python爬虫（8）爬取tuchong网站美图', 'read_num': 6060, 'index': 112}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/68944885', 'acticle_title': '原 python爬虫——爬取链家房价信息（未完待续）', 'read_num': 6185, 'index': 113}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70209450', 'acticle_title': '原 python使用代理访问网站', 'read_num': 6193, 'index': 114}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71168993', 'acticle_title': '转 webdriver+selenium面试总结', 'read_num': 6374, 'index': 115}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/68061256', 'acticle_title': '原 02_python安装错误——2502、2503错误', 'read_num': 6483, 'index': 116}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71123066', 'acticle_title': '原 python——接收处理外带的参数', 'read_num': 7459, 'index': 117}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/68496603', 'acticle_title': '转 Python面试必须要看的15个问题', 'read_num': 7477, 'index': 118}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70175619', 'acticle_title': '原 python爬虫(13)爬取百度贴吧帖子', 'read_num': 7619, 'index': 119}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70766993', 'acticle_title': '原 python_获取当前代码行号_获取当前运行的类名和函数名的方法', 'read_num': 7645, 'index': 120}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71173514', 'acticle_title': '原 python爬虫（11）身边的搜索专家——获取百度搜索结果', 'read_num': 7770, 'index': 121}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70674353', 'acticle_title': '原 python_制作自己的函数库', 'read_num': 7908, 'index': 122}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62985485', 'acticle_title': '原 python爬虫(14)获取淘宝MM个人信息及照片（下）（windows版本）', 'read_num': 7990, 'index': 123}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71326756', 'acticle_title': '原 使用notepad++开发python的配置——代码缩进、自动补齐、运行', 'read_num': 8389, 'index': 124}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60583129', 'acticle_title': '原 python爬虫（6）爬取糗事百科', 'read_num': 8788, 'index': 125}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71081165', 'acticle_title': '转 python安装scipy 遇到的问题', 'read_num': 9595, 'index': 126}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70766654', 'acticle_title': '转 python_python中try except处理程序异常的三种常用方法', 'read_num': 9897, 'index': 127}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70843655', 'acticle_title': '转 shell for循环1到100', 'read_num': 10421, 'index': 128}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/60146843', 'acticle_title': "原 python编译错误(1)字符编码问题UnicodeDecodeError: 'ascii' codec", 'read_num': 10838, 'index': 129}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62894826', 'acticle_title': '原 python爬虫(14)获取淘宝MM个人信息及照片（中）', 'read_num': 11136, 'index': 130}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/62418857', 'acticle_title': '原 python爬虫（9）获取动态搞笑图片', 'read_num': 11543, 'index': 131}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/51801918', 'acticle_title': '原 python爬虫（2）爬取游民星空网的图片', 'read_num': 13661, 'index': 132}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71082263', 'acticle_title': '原 python爬虫(20)使用真实浏览器打开网页的两种方法', 'read_num': 16160, 'index': 133}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/51879501', 'acticle_title': '原 python爬虫（1）下载任意网页图片', 'read_num': 16323, 'index': 134}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/51798833', 'acticle_title': '原 python爬虫(15)爬取百度百科字条_精品', 'read_num': 17306, 'index': 135}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/65631698', 'acticle_title': '原 python爬虫(16)使用scrapy框架爬取顶点小说网', 'read_num': 17652, 'index': 136}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/46800537', 'acticle_title': '原 C语言常见面试题（经典中的经典）', 'read_num': 19962, 'index': 137}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/71126591', 'acticle_title': '原 python爬虫（18）爬取微信公众号内容——绘制词云', 'read_num': 20565, 'index': 138}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70160059', 'acticle_title': '原 python爬虫（17）爬出新高度_抓取微信公众号文章（selenium+phantomjs）（下）（windows版本）', 'read_num': 22474, 'index': 139}, {'articles_url': 'https://blog.csdn.net/qiqiyingse/article/details/70050113', 'acticle_title': '原 python爬虫(17)爬出新高度_抓取微信公众号文章（selenium+phantomjs）（上）', 'read_num': 32994, 'index': 140}]

	def get_html_by_request(self,url):
		logger(u'开始使用 request 获取的网页为：%s' %  url)
		try:
			html = self.mySession.get(url, headers=self.headers, timeout=self.timeout)
			return html.content
		except Exception as e:
			logger(e)	

	def get_selenium_js_html(self, url):
		
		#Selenim不再支持PhantomJS，请使用headless version 的Chrome或者Firefox替代
		#因此程序执行到这里会有警告
		#driver = webdriver.PhantomJS(executable_path=self.phantomjs_path)	#windows
		driver = webdriver.PhantomJS()	#linux
		'''

		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--disable-gpu')
		driver = webdriver.Chrome(executable_path=self.chromedriver_path,chrome_options=chrome_options)
		'''
		logger(u'开始使用 phantomjs 加载网页：%s' %  url)
		try:
			driver.get(url) 
			time.sleep(2) 
			# 执行js得到整个页面内容
			html = driver.execute_script("return document.documentElement.outerHTML")
			
			driver.close()
			return html
		except Exception as e:
			logger(e)
	
	def parse_html_by_pyquery(self, html):
		if not html:
			logger("获得的网页有问题， 请检查。。。")
		else:
			logger('转换网页成功')
			return pq(html)

	def get_pageNumber(self,doc):
		#print (doc)
		#numcontent=doc('div[class=ui-paging-container]')
		numcontent=doc('li[class=ui-pager]')
		page_number=int(numcontent[len(numcontent)-1].text.strip())
		#page_number =int(int(page_number) * 2.5)+1 #以防万一，偶尔还是需要转换的
		logger('current blogger has page num is  %s' % page_number)
		return page_number

	def get_artilcle_list(self,doc):
		logger('start to get article list...')
		acrticle_list=doc('div[class="article-item-box csdn-tracking-statistics"]')
		logger(len(acrticle_list))
		for acrticle in acrticle_list.items():
			tmp={}
			tmp['文章标题']=acrticle('h4')('a').text().strip()
			tmp['文章地址']=acrticle('h4')('a').attr('href')
			if('yoyo_liyy' not in tmp['文章地址']):
				'''
				print(acrticle('div')('p'))
				print(acrticle('div')('p'))
				'''
				read_num_content=acrticle('span[class=read-num]')('span')[1].text.strip()
				#print(read_num_content)
				tmp['阅读数']=int(re.sub("\D","",read_num_content))	
				#print("tmp['阅读数'] =%s" % tmp['阅读数'])

			
				read_num_content=acrticle('span[class=read-num]')('span')[3].text.strip()
				#print('read_num_content = %s' % read_num_content)
				tmp['评论数']=int(re.sub("\D","",read_num_content))
				#print("tmp['评论数'] =%d" % tmp['评论数'])
			


				logger(tmp['文章地址'])
			
				self.contentList.append(tmp)
			
	#自定义排序功能，按照关键字对列表进行排序,然后将索引添加到字典中
	def mysort(self,listname,keywords,reverse=1):
		'''
		Parater:
			listname:需要处理的list
			keywords:按照keywords进行排序
			reverse：正序还是逆序,1为正序，0为逆序
		'''
		from functools import cmp_to_key
		if reverse:
			newlist=sorted(listname,key=cmp_to_key(lambda x,y:x[keywords]-y[keywords]) )
		else:
			newlist=sorted(listname,key=cmp_to_key(lambda x,y:y[keywords]-x[keywords]))
		for item in newlist:
			item['排行'] = newlist.index(item)+1
		return newlist

	def run(self):
		#第一步，获取页码数目
		main_html=self.get_selenium_js_html(self.csdn_url)
		main_doc=self.parse_html_by_pyquery(main_html)
		page_number=self.get_pageNumber(main_doc)

		
		#第二步，查找文章list
		for i in range(1,int(page_number)+1):
			new_url=self.page_base_url+str(i)
			acrticle_html=self.get_html_by_request(new_url)

			acrticle_doc=self.parse_html_by_pyquery(acrticle_html)
			self.get_artilcle_list(acrticle_doc)

		logger(len(self.contentList))
		self.contentLists = self.mysort(self.contentList,"阅读数",1 )
		logger(self.contentLists)
		return self.contentLists
		
	def testA(self):		
		logger(len(self.mylisttest))
		contentList = self.mysort(self.mylisttest,"阅读数",1)
		aa=[]
		for i in contentList:
			logger("排行 is  [%d] ...阅读数 is: [%d] .... url is [%s]" % (i['index'],i['阅读数'],i['文章地址']))
			tmp="排行 is  [%d] ... 阅读数 is: [%d] .... url is [%s]" % (i['index'],i['阅读数'],i['文章地址'])
			aa.append(tmp)
		return aa

	def testForSortFunc(self):
		Tilist = self.mysort(self.mylisttest,'阅读数',1)
		for i in Tilist:
			print (i['阅读数'])

		Tilist = self.mysort(self.mylisttest,'阅读数',0)
		for i in Tilist:
			print (i['阅读数'])


class SaveDataInExcel():
	def __init__(self,data):
		self.myfoldername='qiqiyingse'
		self.needhandledata=data

	def dealData(self):
		self.create_dir(self.myfoldername)
		filename=self.myfoldername+'/'+self.myfoldername+'.txt'

		self.save_content_to_file(filename,self.needhandledata)
		logger("data write in [text]  finished.....")



		self.handleall()
		#self.run_to_save_info_in_excel(self.needhandledata)
		logger("data write in [excel]  finished.....")
		
	def test(self):
		logger('just a test')
		logger('not just a test ')

	#判断一个文件是否存在	
	def file_is_exist(self,file_name):
		#path = os.path.join(os.getcwd()+'/count/'+file_name)
		#print 'current file [%s] path is [%s]' % (file_name,path)
		is_exists = os.path.exists(file_name)
		return is_exists

	#读取复制一份，并且增加一张新表	
	def read_and_copy_excle(self,excle_file_name):
		read_excel_flag=xlrd.open_workbook(excle_file_name,formatting_info=True)#保存原有格式
		count = len(read_excel_flag.sheets()) #sheet数量
		for r in read_excel_flag.sheets():
			logger(r.name) #sheet名称
		worksheet_copy_flag=copy(read_excel_flag)#复制一份excel
		self.run_to_save_info_in_excel(self.needhandledata,worksheet_copy_flag,excle_file_name)#之后再次插入一份
	def handleall(self):
		#文件存在就复制一份，并在其表的后面插入一个，不存在就新创建一个
		excle_file_name=self.myfoldername+'/'+time.strftime('%Y-%m-%d')+'.xls'
		if self.file_is_exist(excle_file_name):
			logger('file 【%s】 exist ' % excle_file_name)
			self.read_and_copy_excle(excle_file_name)#复制一个excle并追加一个sheet页
		else:
			logger ('file 【%s】is not  exist, will create it ' % excle_file_name)
			excel_flag=xlwt.Workbook()#新建excel工作薄
			self.run_to_save_info_in_excel(self.needhandledata,excel_flag,excle_file_name)
	

	#设置单元格格式
	def set_style(self,name,height,bold,color_index):
		style = xlwt.XFStyle() # 初始化样式
		
		font = xlwt.Font() # 为样式创建字体
		font.name = name # 字体名称
		font.bold = bold #字体加粗
		font.color_index = color_index #字体颜色， 但是貌似无效
		font.height = height
		
		borders= xlwt.Borders()#字体边框
		borders.left= 6
		borders.right= 6
		borders.top= 6
		borders.bottom= 6
		
		style.font = font
		if bold:
			style.borders = borders
		return style	
	
	#将内容存贮到excel中,数据，excel的句柄，文件名字
	def run_to_save_info_in_excel(self,data,excel_w,excle_file_name):
		logger('start save info into excel')
		#excel_w=Workbook()
		#excel_table_name=time.strftime('%Y-%m-%d')
		excel_sheet_name=time.strftime('%Y-%m-%d_%H-%M-%S')
		excel_content_handler=excel_w.add_sheet(excel_sheet_name) 
		
		first_line=[key for key,value in data[0].items()]
		#first_line=[u'标题',u'文章地址',u'阅读次数',u'评论次数',u'排名']
		
		for i in range(0,len(first_line)):
			excel_content_handler.write(0,i,first_line[i],self.set_style('Times New Roman',220,True,0xaaccee))
			
		
		style = xlwt.easyxf('font:height 240, color-index red, bold on;align: wrap on, vert centre, horiz left');
		style2 = xlwt.easyxf('font:height 240, color-index blue, bold on;align: wrap on, vert centre,horiz center');
		index=1
		for data_dict in data:
			cols=0
			for data_details in data_dict:
				#excel_content_handler.write(index,cols,data_dict[data_details],self.set_style('Arial',300,False,0xBBCC00+16*index*(cols+1)) )
				#设置行宽
				if cols== 0 or cols == 1:
					excel_content_handler.write(index,cols,data_dict[data_details], style)
					excel_content_handler.col(cols).width=256*60#*len(data_dict[data_details])
				else:
					excel_content_handler.write(index,cols,data_dict[data_details], style2)
					excel_content_handler.col(cols).width=256*10#*len(data_dict[data_details])
				cols +=1
			index +=1
		excel_w.save(excle_file_name)

		
	#存储文章到本地	
	def save_content_to_file(self,title,content):
		logger('start to write info in [text]...')
		with open(title, 'w',encoding='utf-8') as f:
			for info_dict in content:
				f.write(str(info_dict)+'\n')
				for info in info_dict:
					#logger((info,info_dict[info]))
					#f.write(str(info)+str(info_dict[info])+'\n')
					f.write(str(info_dict[info])+'\t\t\t\t')
				f.write('\n')
	def create_dir(self,dirname):
		if not os.path.exists(dirname):
			os.makedirs(dirname)
			logger(" %s  not exists, create it" % dirname)
		else:
			logger("dirname already exist, didn't need to creat")


class RunUrlInBrowser():	
	def getUrlFromData(self,data):
		'''
		#用这种方式提取列表比较常规，但是代码也多
		urllist=[]
		for url in self.listData:
			urllist.append(url['articles_url'])
		return urllist	
		'''	
		return  [data_info['文章地址']  for data_info in data]
	def LoadUrltoLocalBrowser(self,urllist):
		import webbrowser as web
		t=5
		while t:
			for i in range(0,6):
				
				logger(urllist[i])
				web.open_new_tab(urllist[i])
				time.sleep(2)
				web.open_new_tab(urllist[random.randint(20,140)])
				time.sleep(2)
			time.sleep(5)
			os.system('taskkill /f /IM chrome.exe')
			#os.system('taskkill /f /IM firefox.exe')
			#os.system('taskkill /f /IM MicrosoftEdgeCP.exe')
			time.sleep(2)
			t=t-1 

	def LoadUrlAccordingtoLocalBrowser(self,data):
		import webbrowser as web
		urllist=self.getUrlFromData(data)
		t=10
		while t:
			for i in range(0,5):
				
				logger(urllist[i])
				web.open_new_tab(urllist[i])
				time.sleep(0.5)
				web.open_new_tab(urllist[random.randint(20,140)])
				time.sleep(1)
			os.system('taskkill /f /IM chrome.exe')
			#os.system('taskkill /f /IM firefox.exe')
			#os.system('taskkill /f /IM MicrosoftEdgeCP.exe')
			time.sleep(1)
			t=t-1

#获取CSDN文章列表，并存贮到excel,txt文本，mongoDB中		
def welcom():
	print(''.center(50,'*'))
	print('   Welcome to Spider of CSDN   '.center(50,'*'))
	print('   Created on 2018-08-20   '.center(50,'*'))
	print('   @author: Jimy _Fengqi   '.center(50,'*'))
	print(''.center(50,'*'))

	mycsdn=CSDNSpider()
	data = mycsdn.run()
	
	
	#先把数据存贮到excel,因为excel部分没有对数据进行另外的处理
	myHandler=SaveDataInExcel(data)
	myHandler.dealData()
	
	#再把数据存贮到数据库
	mydb=PymongoDataSave(data)
	mydb.handleData()
	
#仅仅遍历pymongodb 数据库		
def getDBlist():
	mydb=PymongoDataSave()

#从数据库读取地址列表，用浏览器打开
def openwithbrowser():
	mydb=PymongoDataSave()
	data=mydb.getURLlistdata()

	print(data)
	#myBrowser=RunUrlInBrowser()
	#myBrowser.LoadUrltoLocalBrowser(data)

if __name__ == '__main__':
	#引用类中的方法的时候，这里类本身不能有括号 ，就是不能写成myHandler().test() 
	welcom()
	openwithbrowser()

	
	#最后把用网页打开
	#myBrowser=RunUrlInBrowser(data)
	#myBrowser.LoadUrlAccordingtoLocalBrowser()
	

	
	#data=mycsdn.mylisttest
	#myHandler=HandleMyData(data)
	#myHandler.test()                    #引用类中的方法的时候，这里类本身不能有括号 ，就是不能写成myHandler().test() 
	#myHandler.dealData()

	#mycsdn.run()
	#mycsdn.testfunc()