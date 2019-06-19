# -*- coding: utf-8 -*-
# @Date     : 2019-02-13 11:08:25
# @Author   : Jimy_Fengqi (jmps515@163.com)
# @Link     : https://blog.csdn.net/qiqiyingse
# @Version  : V1.0
# @pyVersion: 3.6

import time,os,random


data=['https://blog.csdn.net/qiqiyingse/article/details/90059586', 'https://blog.csdn.net/qiqiyingse/article/details/90265870',
'https://blog.csdn.net/qiqiyingse/article/details/90518906',
'https://blog.csdn.net/qiqiyingse/article/details/90440377',
'https://blog.csdn.net/qiqiyingse/article/details/90059586', 
 'https://blog.csdn.net/qiqiyingse/article/details/90176028', 'https://blog.csdn.net/qiqiyingse/article/details/87804114', 
 'https://blog.csdn.net/qiqiyingse/article/details/87811263', 'https://blog.csdn.net/qiqiyingse/article/details/87935999', 
 'https://blog.csdn.net/qiqiyingse/article/details/79473830', 'https://blog.csdn.net/qiqiyingse/article/details/77855473',
 'https://blog.csdn.net/qiqiyingse/article/details/90719760', 'https://blog.csdn.net/qiqiyingse/article/details/72540866',
 'https://blog.csdn.net/qiqiyingse/article/details/72453537', 'https://blog.csdn.net/qiqiyingse/article/details/82157080',
 'https://blog.csdn.net/qiqiyingse/article/details/82256348', 'https://blog.csdn.net/qiqiyingse/article/details/83343710', 
 'https://blog.csdn.net/qiqiyingse/article/details/72961382', 'https://blog.csdn.net/qiqiyingse/article/details/72898831', 
 'https://blog.csdn.net/qiqiyingse/article/details/84791879', 'https://blog.csdn.net/qiqiyingse/article/details/80269610', 
 'https://blog.csdn.net/qiqiyingse/article/details/79471634', 'https://blog.csdn.net/qiqiyingse/article/details/71643828', 
 'https://blog.csdn.net/qiqiyingse/article/details/71514942', 'https://blog.csdn.net/qiqiyingse/article/details/77835705', 
 'https://blog.csdn.net/qiqiyingse/article/details/83659396', 'https://blog.csdn.net/qiqiyingse/article/details/74004472', 
 'https://blog.csdn.net/qiqiyingse/article/details/71580496', 'https://blog.csdn.net/qiqiyingse/article/details/71756381', 
 'https://blog.csdn.net/qiqiyingse/article/details/83114168', 'https://blog.csdn.net/qiqiyingse/article/details/82901412', 
 'https://blog.csdn.net/qiqiyingse/article/details/71226818',  'https://blog.csdn.net/qiqiyingse/article/details/79471056', 
 'https://blog.csdn.net/qiqiyingse/article/details/71216102',  'https://blog.csdn.net/qiqiyingse/article/details/71232015', 
 'https://blog.csdn.net/qiqiyingse/article/details/71405436', 'https://blog.csdn.net/qiqiyingse/article/details/81668345', 
 'https://blog.csdn.net/qiqiyingse/article/details/72553279', 'https://blog.csdn.net/qiqiyingse/article/details/83621550', 'https://blog.csdn.net/qiqiyingse/article/details/71123322', 'https://blog.csdn.net/qiqiyingse/article/details/81567080', 'https://blog.csdn.net/qiqiyingse/article/details/86677773', 'https://blog.csdn.net/qiqiyingse/article/details/59483706', 'https://blog.csdn.net/qiqiyingse/article/details/85005537', 'https://blog.csdn.net/qiqiyingse/article/details/71227451', 'https://blog.csdn.net/qiqiyingse/article/details/84792202', 'https://blog.csdn.net/qiqiyingse/article/details/85130923', 'https://blog.csdn.net/qiqiyingse/article/details/59483629', 'https://blog.csdn.net/qiqiyingse/article/details/70048820', 'https://blog.csdn.net/qiqiyingse/article/details/59112479', 'https://blog.csdn.net/qiqiyingse/article/details/60132246', 'https://blog.csdn.net/qiqiyingse/article/details/70143777', 'https://blog.csdn.net/qiqiyingse/article/details/60582816', 'https://blog.csdn.net/qiqiyingse/article/details/59481693', 'https://blog.csdn.net/qiqiyingse/article/details/86677756', 'https://blog.csdn.net/qiqiyingse/article/details/55260352', 'https://blog.csdn.net/qiqiyingse/article/details/82841369', 'https://blog.csdn.net/qiqiyingse/article/details/60582751', 'https://blog.csdn.net/qiqiyingse/article/details/61197123', 'https://blog.csdn.net/qiqiyingse/article/details/82985386', 'https://blog.csdn.net/qiqiyingse/article/details/82977886', 'https://blog.csdn.net/qiqiyingse/article/details/86677738', 'https://blog.csdn.net/qiqiyingse/article/details/84567189', 'https://blog.csdn.net/qiqiyingse/article/details/70145804', 'https://blog.csdn.net/qiqiyingse/article/details/83011821', 'https://blog.csdn.net/qiqiyingse/article/details/83538294', 'https://blog.csdn.net/qiqiyingse/article/details/86677666', 'https://blog.csdn.net/qiqiyingse/article/details/70855457', 'https://blog.csdn.net/qiqiyingse/article/details/70161637', 'https://blog.csdn.net/qiqiyingse/article/details/68926007', 'https://blog.csdn.net/qiqiyingse/article/details/59113090', 'https://blog.csdn.net/qiqiyingse/article/details/70138912', 'https://blog.csdn.net/qiqiyingse/article/details/55259304', 'https://blog.csdn.net/qiqiyingse/article/details/71131120', 'https://blog.csdn.net/qiqiyingse/article/details/71344110', 'https://blog.csdn.net/qiqiyingse/article/details/71308389', 'https://blog.csdn.net/qiqiyingse/article/details/62896264', 'https://blog.csdn.net/qiqiyingse/article/details/69944173', 'https://blog.csdn.net/qiqiyingse/article/details/71123348', 'https://blog.csdn.net/qiqiyingse/article/details/60583419', 'https://blog.csdn.net/qiqiyingse/article/details/59112715', 'https://blog.csdn.net/qiqiyingse/article/details/59483966', 'https://blog.csdn.net/qiqiyingse/article/details/46800097', 'https://blog.csdn.net/qiqiyingse/article/details/70046543', 'https://blog.csdn.net/qiqiyingse/article/details/70209450', 'https://blog.csdn.net/qiqiyingse/article/details/71168993', 'https://blog.csdn.net/qiqiyingse/article/details/68496603', 'https://blog.csdn.net/qiqiyingse/article/details/62985485', 'https://blog.csdn.net/qiqiyingse/article/details/70674353', 'https://blog.csdn.net/qiqiyingse/article/details/60583129', 'https://blog.csdn.net/qiqiyingse/article/details/71081165', 'https://blog.csdn.net/qiqiyingse/article/details/70766993', 'https://blog.csdn.net/qiqiyingse/article/details/71326756', 'https://blog.csdn.net/qiqiyingse/article/details/70843655', 'https://blog.csdn.net/qiqiyingse/article/details/70160059', 'https://blog.csdn.net/qiqiyingse/article/details/70050113', 'https://blog.csdn.net/qiqiyingse/article/details/90202717', 'https://blog.csdn.net/qiqiyingse/article/details/90293322', 'https://blog.csdn.net/qiqiyingse/article/details/89155143', 'https://blog.csdn.net/qiqiyingse/article/details/88189193', 'https://blog.csdn.net/qiqiyingse/article/details/88188491', 'https://blog.csdn.net/qiqiyingse/article/details/88242172', 'https://blog.csdn.net/qiqiyingse/article/details/88126213', 'https://blog.csdn.net/qiqiyingse/article/details/88124259', 'https://blog.csdn.net/qiqiyingse/article/details/88241862', 'https://blog.csdn.net/qiqiyingse/article/details/88239317', 'https://blog.csdn.net/qiqiyingse/article/details/87976378', 'https://blog.csdn.net/qiqiyingse/article/details/88243138', 'https://blog.csdn.net/qiqiyingse/article/details/88240335', 'https://blog.csdn.net/qiqiyingse/article/details/87974523', 'https://blog.csdn.net/qiqiyingse/article/details/85127568', 'https://blog.csdn.net/qiqiyingse/article/details/78141474', 'https://blog.csdn.net/qiqiyingse/article/details/81776735', 'https://blog.csdn.net/qiqiyingse/article/details/71543110', 'https://blog.csdn.net/qiqiyingse/article/details/84950497', 'https://blog.csdn.net/qiqiyingse/article/details/78141487', 'https://blog.csdn.net/qiqiyingse/article/details/83343752', 'https://blog.csdn.net/qiqiyingse/article/details/74004388', 'https://blog.csdn.net/qiqiyingse/article/details/71544282', 'https://blog.csdn.net/qiqiyingse/article/details/71647261', 'https://blog.csdn.net/qiqiyingse/article/details/82256184', 'https://blog.csdn.net/qiqiyingse/article/details/82865870', 'https://blog.csdn.net/qiqiyingse/article/details/72566001', 'https://blog.csdn.net/qiqiyingse/article/details/81281658', 'https://blog.csdn.net/qiqiyingse/article/details/72953832', 'https://blog.csdn.net/qiqiyingse/article/details/71757964', 'https://blog.csdn.net/qiqiyingse/article/details/78132072', 'https://blog.csdn.net/qiqiyingse/article/details/81668517', 'https://blog.csdn.net/qiqiyingse/article/details/78210646', 'https://blog.csdn.net/qiqiyingse/article/details/71747671', 'https://blog.csdn.net/qiqiyingse/article/details/72633533', 'https://blog.csdn.net/qiqiyingse/article/details/77745548', 'https://blog.csdn.net/qiqiyingse/article/details/81540418', 'https://blog.csdn.net/qiqiyingse/article/details/72558839', 'https://blog.csdn.net/qiqiyingse/article/details/71547716', 'https://blog.csdn.net/qiqiyingse/article/details/71678011', 'https://blog.csdn.net/qiqiyingse/article/details/77749109', 'https://blog.csdn.net/qiqiyingse/article/details/87814582', 'https://blog.csdn.net/qiqiyingse/article/details/87937947', 'https://blog.csdn.net/qiqiyingse/article/details/72553276', 'https://blog.csdn.net/qiqiyingse/article/details/72285927', 'https://blog.csdn.net/qiqiyingse/article/details/78225394', 'https://blog.csdn.net/qiqiyingse/article/details/88031877', 'https://blog.csdn.net/qiqiyingse/article/details/81980458', 'https://blog.csdn.net/qiqiyingse/article/details/87937267', 'https://blog.csdn.net/qiqiyingse/article/details/83747208', 'https://blog.csdn.net/qiqiyingse/article/details/71640203', 'https://blog.csdn.net/qiqiyingse/article/details/71172347', 'https://blog.csdn.net/qiqiyingse/article/details/85112139', 'https://blog.csdn.net/qiqiyingse/article/details/84950002', 'https://blog.csdn.net/qiqiyingse/article/details/84792242', 'https://blog.csdn.net/qiqiyingse/article/details/59112217', 'https://blog.csdn.net/qiqiyingse/article/details/60144027', 'https://blog.csdn.net/qiqiyingse/article/details/59488018', 'https://blog.csdn.net/qiqiyingse/article/details/85115212', 'https://blog.csdn.net/qiqiyingse/article/details/79487514', 'https://blog.csdn.net/qiqiyingse/article/details/83747113', 'https://blog.csdn.net/qiqiyingse/article/details/55517278', 'https://blog.csdn.net/qiqiyingse/article/details/64522690', 'https://blog.csdn.net/qiqiyingse/article/details/70208940', 'https://blog.csdn.net/qiqiyingse/article/details/85123431', 'https://blog.csdn.net/qiqiyingse/article/details/60572338', 'https://blog.csdn.net/qiqiyingse/article/details/72633711', 'https://blog.csdn.net/qiqiyingse/article/details/62427733', 'https://blog.csdn.net/qiqiyingse/article/details/60129630', 'https://blog.csdn.net/qiqiyingse/article/details/83993098', 'https://blog.csdn.net/qiqiyingse/article/details/70172218', 'https://blog.csdn.net/qiqiyingse/article/details/78501034', 'https://blog.csdn.net/qiqiyingse/article/details/70843626', 'https://blog.csdn.net/qiqiyingse/article/details/62427155', 'https://blog.csdn.net/qiqiyingse/article/details/59526995', 'https://blog.csdn.net/qiqiyingse/article/details/59483536', 'https://blog.csdn.net/qiqiyingse/article/details/62231679', 'https://blog.csdn.net/qiqiyingse/article/details/46799543', 'https://blog.csdn.net/qiqiyingse/article/details/68061256', 'https://blog.csdn.net/qiqiyingse/article/details/70855068', 'https://blog.csdn.net/qiqiyingse/article/details/68944885', 'https://blog.csdn.net/qiqiyingse/article/details/70049591', 'https://blog.csdn.net/qiqiyingse/article/details/71616418', 'https://blog.csdn.net/qiqiyingse/article/details/59502402', 'https://blog.csdn.net/qiqiyingse/article/details/70175619', 'https://blog.csdn.net/qiqiyingse/article/details/71123066', 'https://blog.csdn.net/qiqiyingse/article/details/71173514', 'https://blog.csdn.net/qiqiyingse/article/details/60146843', 'https://blog.csdn.net/qiqiyingse/article/details/62418857', 'https://blog.csdn.net/qiqiyingse/article/details/62894826', 'https://blog.csdn.net/qiqiyingse/article/details/51801918', 'https://blog.csdn.net/qiqiyingse/article/details/70766654', 'https://blog.csdn.net/qiqiyingse/article/details/51798833', 'https://blog.csdn.net/qiqiyingse/article/details/65631698', 'https://blog.csdn.net/qiqiyingse/article/details/71082263', 'https://blog.csdn.net/qiqiyingse/article/details/46800537', 'https://blog.csdn.net/qiqiyingse/article/details/71126591', 'https://blog.csdn.net/qiqiyingse/article/details/90697835', 'https://blog.csdn.net/qiqiyingse/article/details/91518343', 'https://blog.csdn.net/qiqiyingse/article/details/91972835', 'https://blog.csdn.net/qiqiyingse/article/details/89314156', 'https://blog.csdn.net/qiqiyingse/article/details/90719866', 'https://blog.csdn.net/qiqiyingse/article/details/90447458', 'https://blog.csdn.net/qiqiyingse/article/details/90518906', 'https://blog.csdn.net/qiqiyingse/article/details/90440377', 'https://blog.csdn.net/qiqiyingse/article/details/81565263', 'https://blog.csdn.net/qiqiyingse/article/details/79442645', 'https://blog.csdn.net/qiqiyingse/article/details/77747777', 'https://blog.csdn.net/qiqiyingse/article/details/82977864', 'https://blog.csdn.net/qiqiyingse/article/details/71218711', 'https://blog.csdn.net/qiqiyingse/article/details/71122905', 'https://blog.csdn.net/qiqiyingse/article/details/67641261', 'https://blog.csdn.net/qiqiyingse/article/details/85124723', 'https://blog.csdn.net/qiqiyingse/article/details/70125444', 'https://blog.csdn.net/qiqiyingse/article/details/60144578', 'https://blog.csdn.net/qiqiyingse/article/details/46800751', 'https://blog.csdn.net/qiqiyingse/article/details/62236845', 'https://blog.csdn.net/qiqiyingse/article/details/71325615',
 'https://blog.csdn.net/qiqiyingse/article/details/51879501']
 



class RunUrlInBrowser():	
	def LoadUrltoLocalBrowser(self,urllist):
		import webbrowser as web
		t=100
		while t:
			for i in range(0,5):
				
				print(urllist[i])
				web.open_new_tab(urllist[i])
				time.sleep(2)
				web.open_new_tab(urllist[random.randint(20,140)])
				time.sleep(2)
			time.sleep(5)
			os.system('taskkill /f /IM iexplore.exe')
			#os.system('taskkill /f /IM chrome.exe')
			#os.system('taskkill /f /IM firefox.exe')
			#os.system('taskkill /f /IM MicrosoftEdgeCP.exe')
			time.sleep(2)
			t=t-1 


def openwithbrowser():
	myBrowser=RunUrlInBrowser()
	myBrowser.LoadUrltoLocalBrowser(data)

if __name__ == '__main__':
	#引用类中的方法的时候，这里类本身不能有括号 ，就是不能写成myHandler().test() 
	#welcom()
	openwithbrowser()				
