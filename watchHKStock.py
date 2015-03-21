#coding=utf-8
import urllib2  
import string
import platform;
import win32api, win32con, win32gui
import time
import copy

systemName = platform.system(); 
pythonVersion = platform.python_version();
uname = platform.uname();
print "System and machine: %s, Python version: %s"%(uname, pythonVersion);

i = 0 
destPrice = 11.1000
endTagStrList = [
			'</span></span> <span class="up_g time_rtq_content">',
			'</span></span></span></span></span></span>',
			]
stockUrlList = [
			'http://hk.finance.yahoo.com/q?s=0992.HK%2C+&ql=1', #雅虎香港
			'http://www.aastocks.com/tc/ltp/rtquote.aspx?symbol=992', #阿斯达克
			]
sourceIdx = 1
while 1:
	i = i + 1
	currtime = time.localtime()
	timeStr = time.strftime("%d %b %Y %H:%M:%S", currtime)
	#print currtime.tm_hour
	try:
		request = urllib2.Request(stockUrlList[sourceIdx], unverifiable=True)
		response = urllib2.urlopen(request, timeout = 30) 
		htmlContent = response.read()
	except:
		print '%d. %s Some error/exception occurred. Let me try again' %(i, timeStr)
		continue
	else:
		endPos = htmlContent.find(endTagStrList[sourceIdx])
		beginPos = htmlContent.find('>', endPos - 10) + 1
		#print "%d, %d" %(beginPos, endPos)
		priceStr = htmlContent[beginPos : endPos]
		print "%d. %s HK992 current price: %s" %(i, timeStr, priceStr)
		currPrice = string.atof(priceStr)
		if currPrice >= destPrice:
			win32api.MessageBox(0, priceStr, "current price", win32con.MB_SETFOREGROUND)
		#finishTime = time.localtime()
		#print "cost time: %d s" %(finishTime.tm_sec - currtime.tm_sec)

		if currtime.tm_hour >= 16 or currtime.tm_hour < 9:
			print "closing quotation now, finish watch"
			break
	time.sleep(30)