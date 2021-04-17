import json
import traceback
import hashlib
import requests

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from resource.models import resource
from user.models import userInfo, download, store
from resource import views 
from profession.models import profession
import service.views as serviceView

# 将传入字符串参数pwd使用MD5算法加密并返回，用于密码加密存储
def MD5(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf-8'))
    salt_password = md5.hexdigest()
    return salt_password

@csrf_exempt
def hello(request):
	return HttpResponse("Hello User")

@csrf_exempt
def getAllUserInfo(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		qset = userInfo.objects.all()
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			res['data'] = DATA
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

@csrf_exempt
def getAllDownload(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		qset = download.objects.all()
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			res['data'] = DATA
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

@csrf_exempt
def getAllStore(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		qset = store.objects.all()
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			res['data'] = DATA
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 账户注册
@csrf_exempt
def register(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_account = request.POST['account']
		user_nick_name = request.POST['nickName']
		user_password = request.POST['password']
		salt_password = MD5(user_password)
	
		qset = userInfo.objects.filter(Q(account=user_account) | Q(studentID=user_account),status=1)
		if len(qset):
			res = {'code': -1, 'msg': '账号已存在', 'data':{}}
			return HttpResponse(json.dumps(res))

		qset = userInfo.objects.filter(nickName=user_nick_name,status=1)
		if len(qset):
			res = {'code': -2, 'msg': '昵称已存在', 'data':{}}
			return HttpResponse(json.dumps(res))

		if serviceView.isLegalText(user_nick_name) == False:
			res = {'code': -3, 'msg': '昵称违规', 'data': {}}
			print(res)
			return HttpResponse(json.dumps(res))

		insert = userInfo(account=user_account,nickName=user_nick_name,password=salt_password,status=1)
		insert.save()
		
		user_info = userInfo.objects.filter(account=user_account)
		DATA = json.loads(serializers.serialize("json", user_info))
		res['data'] = DATA[0]['fields']
		res['data']['UserID'] = DATA[0]['pk']
		del res['data']['password']
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 账户登录
@csrf_exempt
def login(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_account = request.POST['account']
		user_password = request.POST['password']
		salt_password = MD5(user_password)
	
		qset = userInfo.objects.filter(Q(account=user_account) | Q(studentID=user_account),status=1)
		if len(qset) == 0:
			res = {'code': -1, 'msg': '账号或学号不存在', 'data':{}}
			return HttpResponse(json.dumps(res))

		user_info = userInfo.objects.filter(Q(account=user_account) | Q(studentID=user_account),password=salt_password,status=1)
		if len(user_info) == 0:
			res = {'code': -2, 'msg': '密码错误', 'data':{}}
			return HttpResponse(json.dumps(res))

		DATA = json.loads(serializers.serialize("json", user_info))
		res['data'] = DATA[0]['fields']
		res['data']['UserID'] = DATA[0]['pk']
		del res['data']['password']
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 华师大用户身份认证
@csrf_exempt
def authentication(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_id= request.POST['UserID']
		student_id= request.POST['studentID']
		student_password = request.POST['studentPassword']
		
		url = 'http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx'
		params = {"id": student_id, "pwd": student_password, "act": 'login'}
		r = requests.post(url, data=params, timeout=5).json()

		if r['ret'] == 1:
			try:
				u = userInfo.objects.get(UserID=user_id)
				u.studentID = student_id
				u.studentName = r['data']['name']
				u.role=2
				u.save()
			except userInfo.DoesNotExist:
				res = {'code': -1, 'msg': '用户不存在', 'data': {}}
		else:
			res = {'code': -2, 'msg': '认证失败', 'data': {}}
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 密码修改
@csrf_exempt
def modifyPassword(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_id= request.POST['UserID']
		old_password= request.POST['oldPassword']
		new_password = request.POST['newPassword']
		salt_old_password = MD5(old_password)
		salt_new_password = MD5(new_password)
		
		user_info = userInfo.objects.get(UserID=user_id)

		if user_info.password != salt_old_password:
			res = {'code': -1, 'msg': '原密码错误', 'data':{}}
			return HttpResponse(json.dumps(res))

		user_info.password = salt_new_password
		user_info.save()
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 昵称修改
@csrf_exempt
def modifyNickname(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_id= request.POST['UserID']
		nick_name= request.POST['nickName']
		qset = userInfo.objects.filter(nickName=nick_name,status=1)
		if len(qset):
			res = {'code': -1, 'msg': '昵称已存在', 'data':{}}
			return HttpResponse(json.dumps(res))	

		if serviceView.isLegalText(nick_name) == False:
			res = {'code': -2, 'msg': '昵称违规', 'data': {}}
			print(res)
			return HttpResponse(json.dumps(res))

		user_info = userInfo.objects.get(UserID=user_id)
		user_info.nickName = nick_name
		user_info.save()
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 用户点击收藏指定资源
@csrf_exempt
def storeResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		resource_id = int(request.POST['ResourceID'])
		user_id= request.POST['UserID']
		
		update = resource.objects.get(ResourceID=resource_id)
		if update.status == 0:
			res = {'code': -1, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))

		qset = store.objects.filter(ResourceID=resource_id,UserID=user_id)
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			current_store = store.objects.get(StoreID=DATA[0]['pk'])
			if current_store.status == 1:
				res = {'code': -2, 'msg': '无法重复收藏', 'data': {}}
				return HttpResponse(json.dumps(res))
			else:
				current_store.status = 1
				current_store.save()
		else:
			insert = store(ResourceID=resource_id,UserID=user_id)
			insert.save()

		update.storeCount = store.objects.filter(ResourceID=resource_id,status=1).count()
		update.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 取消收藏指定资源
@csrf_exempt
def cancelStoreResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		store_id = int(request.POST['StoreID'])

		current_store = store.objects.get(StoreID=store_id)
		update = resource.objects.get(ResourceID=current_store.ResourceID)

		if update.status == 0:
			res = {'code': -1, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))
		if current_store.status == 0:
			res = {'code': -2, 'msg': '无法重复取消收藏', 'data': {}}
			return HttpResponse(json.dumps(res))

		current_store.status = 0
		current_store.save()

		update.storeCount = store.objects.filter(ResourceID=current_store.ResourceID,status=1).count()
		update.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 获取用户收藏的资源列表
@csrf_exempt
def getStoreResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_id = int(request.POST['UserID'])
		
		qset = store.objects.filter(UserID=user_id,status=1).order_by('-ctime')
		if len(qset):
			length = 0
			res['data']['resourceList'] = []
			DATA = json.loads(serializers.serialize("json", qset))
			for item in DATA:
				tmp = {}
				result = views.getResouceBasicInfoByID(item['fields']['ResourceID'])
				if result['code'] == 0:
					tmp = result['data']
					tmp['StoreID'] = item['pk']
					tmp['ResourceID'] = item['fields']['ResourceID']
					res['data']['resourceList'].append(tmp)
					length += 1
			res['data']['length'] = length
				
		else:
			res['data']['length'] = 0

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 用户点击下载指定资源
@csrf_exempt
def downloadResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		resource_id = int(request.POST['ResourceID'])
		user_id= request.POST['UserID']
		
		update = resource.objects.get(ResourceID=resource_id)
		if update.status == 0:
			res = {'code': -1, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))

		qset = download.objects.filter(ResourceID=resource_id,UserID=user_id)
		if len(qset):
			res = {'code': 0, 'msg': '资源已在下载列表中', 'data':{}}
			return HttpResponse(json.dumps(res))

		insert = download(ResourceID=resource_id,UserID=user_id)
		insert.save()

		update.downloadCount = download.objects.filter(ResourceID=resource_id,status=1).count()
		update.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 获取用户下载的资源列表
@csrf_exempt
def getDownloadResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_id = int(request.POST['UserID'])
		
		qset = download.objects.filter(UserID=user_id,status=1).order_by('-ctime')
		if len(qset):
			length = 0
			res['data']['resourceList'] = []
			DATA = json.loads(serializers.serialize("json", qset))
			for item in DATA:
				tmp = {}
				result = views.getResouceBasicInfoByID(item['fields']['ResourceID'])
				if result['code'] == 0:
					tmp = result['data']
					tmp['DownloadID'] = item['pk']
					tmp['ResourceID'] = item['fields']['ResourceID']
					res['data']['resourceList'].append(tmp)	
					length += 1
			res['data']['length'] = length	
		else:
			res['data']['length'] = 0

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 获取用户上传的资源列表
@csrf_exempt
def getUploadResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_id = int(request.POST['UserID'])
		
		qset = resource.objects.filter(UserID=user_id,status=1).order_by('-ctime')
		if len(qset):
			length = 0
			res['data']['resourceList'] = []
			DATA = json.loads(serializers.serialize("json", qset))
			for item in DATA:
				tmp = item['fields']
				tmp['ResourceID'] = item['pk']
				current_profession = profession.objects.get(ProfessionID=item['fields']['ProfessionID'])
				tmp['professionName'] = current_profession.name
				res['data']['resourceList'].append(tmp)	
				length += 1
			res['data']['length'] = length	
		else:
			res['data']['length'] = 0

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 取消上传指定资源
@csrf_exempt
def cancelUploadResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		resource_id = int(request.POST['ResourceID'])
		
		current_upload = resource.objects.get(ResourceID=resource_id)
		if current_upload.status == 0:
			res = {'code': -1, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))

		current_upload.status = 0
		current_upload.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))