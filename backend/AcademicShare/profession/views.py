import json
import traceback

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from profession.models import profession

@csrf_exempt
def hello(request):
	return HttpResponse("Hello Profession")

# 将14个学科大类导入profession模型
@csrf_exempt
def insertProfession(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		password = request.POST['password']
		if password != '19990302':
			res = {'code': -1, 'msg': 'incorrect password', 'data': {}}
			return HttpResponse(json.dumps(res))
		professions = [
			'工学', '理学', '哲学', '经济学',
			'法学', '教育学', '文学', '历史学',
			'农学', '医学', '军事学', '管理学',
			'艺术学', '交叉学科',
		]
		cnt = profession.objects.count()
		if cnt:
			res = {'code': -2, 'msg': 'data already insert', 'data': {}}
			return HttpResponse(json.dumps(res))
		for proName in professions:
			insert = profession(name=proName)
			insert.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 查询所有学科大类
@csrf_exempt
def listProfession(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		qset = profession.objects.filter(status=1)
		if len(qset):
			res['data'] = []
			DATA = json.loads(serializers.serialize("json", qset))
			for item in DATA:
				res['data'].append({'id': item['pk'], 'name': item['fields']['name']})

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))