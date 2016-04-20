#coding=utf-8

import urllib
import urllib2
import json
import string
import sys

appKey = "prhjAiqno3uLzsCevYL8g2wh"
oriWord1 = "不行"
oriWord2 = "animation"
'''
中文	zh	
英语	en
日语	jp
韩语	kor
西班牙语	spa
法语	fra
泰语	th
阿拉伯语	ara
俄罗斯语	ru
葡萄牙语	pt
粤语	yue
文言文	wyw
白话文	zh
自动检测	auto
德语	de	
意大利语	it
荷兰语	nl
希腊语	el
'''
fromLang = "auto"
toLang = "auto"
baiduTransUrl = "http://openapi.baidu.com/public/2.0/bmt/translate?client_id=%s&q=%s%%0A%s&from=%s&to=%s"
url = baiduTransUrl % (appKey, oriWord1, oriWord2, fromLang, toLang)
print "url is: %s" % url

req = urllib2.Request(url)
print req

res_data = urllib2.urlopen(req)
res = res_data.read()
print res

len = len(res)
stIdx = 0
arrSrc = []
arrDst = []
reload(sys)
sys.setdefaultencoding( "utf-8" )
while 1 :
	stIdx = res.find("\"src\":", stIdx) + 6
	if stIdx == -1 + 6 :
		break
	endIdx = res.find("\"", stIdx + 1)
	if endIdx == -1 :
		break
	src = res[stIdx + 1 : endIdx]
	if src.find("\\u") == 0:
		src = src.decode('unicode-escape')
	stIdx = endIdx

	stIdx = res.find("\"dst\":", stIdx) + 6
	if stIdx == -1 + 6 :
		break
	endIdx = res.find("\"", stIdx + 1)
	if endIdx == -1 :
		break
	dst = res[stIdx + 1 : endIdx]
	if dst.find("\\u") == 0:
		dst = dst.decode('unicode-escape')
	stIdx = endIdx

	print "%s\t\t%s" % (src, dst)

'''
list = list(res)
res = "".join(list)
print res
decodeRes = json.dumps(list)
print decodeRes
'''