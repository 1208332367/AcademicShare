import traceback
import time
import json
import requests

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from resource.models import wx_token

# 获取微信平台接口调用凭据（access_token）并返回，用于调用相关API
def getToken():
	try:
		res = ''
		appid = "wx637af67a977cbafb"
		secret = "5072e1e0922cd892512deb079d38f681"
		url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
		
		qset = wx_token.objects.filter(id=1, status=1)
		ctime=int(time.time())
		if len(qset) == 1:
			data = json.loads(serializers.serialize("json", qset))[0]['fields']
			if ctime-data['update_time'] > 7200:
				ctime=int(time.time())

				response = requests.get(url)
				response = response.json()
				wx_token.objects.filter(id=1,status=1).update(access_token=response['access_token'],update_time=ctime)
				return response['access_token']
			else:
				return data['access_token'];
		else:
			response = requests.get(url)
			response = response.json()
			ctime=int(time.time())
			insert = wx_token.objects.create(access_token=response['access_token'],update_time=ctime)
			return response['access_token']

	except Exception as e:
		traceback.print_exc()
		return res

# 判断给定文本是否包含违规内容，用于限制用户的输入
def isLegalText(text):
	token = getToken()
	url = "https://api.weixin.qq.com/wxa/msg_sec_check?access_token=" + token
	data = {
		"content":text.encode("utf-8").decode("latin1")
	}
	headers = {'content-type': 'application/json'}
	# 发起POST请求
	response =requests.post(url, data=json.dumps(data,ensure_ascii=False),headers=headers)
	requests.post(url=url, data=data)
	response = response.json()
	print(response)
	if response['errcode'] == 87014:
		return False
	return True