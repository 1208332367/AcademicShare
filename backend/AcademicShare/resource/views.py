import json
import traceback

import os
import time
import random

from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from AcademicShare import settings
from django.core.files.storage import default_storage
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from django.db.models import Avg
from resource.models import resource, comment, report
from user.models import userInfo
from profession.models import profession
import service.views as serviceView

# 根据resource_id，查询某一资源条的基本信息
def getResouceBasicInfoByID(resource_id):
	res = {'code': -1, 'msg': 'resource not found', 'data':{}}
	try:
		qset = resource.objects.filter(ResourceID=resource_id,status=1)
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			res = {'code': 0, 'msg': 'resource not found', 'data':DATA[0]['fields']}
			current_profession = profession.objects.get(ProfessionID=DATA[0]['fields']['ProfessionID'])
			res['data']['professionName'] = current_profession.name

	except Exception as e:
		res = {'code': -2, 'msg': 'exception occurred', 'data': {}}
		traceback.print_exc()

	return res

@csrf_exempt
def hello(request):
	return HttpResponse("Hello Resource")

@csrf_exempt
def getAllResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		qset = resource.objects.all()
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			res['data'] = DATA
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

@csrf_exempt
def getAllReport(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		qset = report.objects.all()
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			res['data'] = DATA
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 上传并添加资源信息
@csrf_exempt
def uploadFile(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		user_id = int(request.POST['UserID'])
		resource_title = request.POST['title']
		profession_id = int(request.POST['ProfessionID'])
		visit_ctrl = int(request.POST['visitCtrl'])
		resource_intro = request.POST['resource_intro']
		file_extname = request.POST['extname']

		file = request.FILES.get('file')  # 获取上传的文件
		if not file:
			res = {'code': -1, 'msg': '文件为空，请重新上传', 'data':{}}
			return HttpResponse(json.dumps(res))

		if serviceView.isLegalText(resource_title) == False:
			res = {'code': -2, 'msg': '标题内容违规', 'data': {}}
			print(res)
			return HttpResponse(json.dumps(res))

		if serviceView.isLegalText(resource_intro) == False:
			res = {'code': -3, 'msg': '简介内容违规', 'data': {}}
			return HttpResponse(json.dumps(res))

		#设置文件夹名，存放上传的文件
		user_folder = "UserID_" + str(user_id)
		user_dir = os.path.join(settings.FILE_PATH, user_folder)
		if not user_dir:  # 判断是否存在文件夹如果不存在则创建为文件夹
			os.makedirs(user_dir)  # makedirs 创建文件时如果路径不存在会创建这个路径

		#设置文件名
		file_name = time.strftime('%Y%m%d_%H%M%S_',time.localtime()) + str(int(round(time.time() * 1000))) + '_' + str(random.randint(0,10000))
		file_name =  file_name + '.' + file_extname
		file_path = os.path.join(user_dir, file_name).replace('\\', '/')

		#存储文件到指定路径
		default_storage.save(file_path, file)	

		file_size = os.path.getsize(file_path) / 1024.0

		#存储数据到数据库
		local_url = os.path.join(user_folder, file_name).replace('\\', '/')
		insert = resource(UserID=user_id,title=resource_title,fileSize=file_size,localUrl=local_url,ProfessionID=profession_id,visitCtrl=visit_ctrl,intro=resource_intro)
		insert.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 根据ResourceID查询资源详情
@csrf_exempt
def getResouceDetailByID(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		resource_id = int(request.POST['ResourceID'])

		qset = resource.objects.filter(ResourceID=resource_id,status=1)
		if len(qset):
			DATA = json.loads(serializers.serialize("json", qset))
			res['data'] = DATA[0]['fields']
			res['data']['length'] = 1
			res['data']['ResourceID'] = resource_id
			res['data']['webUrl'] = settings.DOMAIN + 'media/files/' + DATA[0]['fields']['localUrl']
			current_profession = profession.objects.get(ProfessionID=DATA[0]['fields']['ProfessionID'])
			res['data']['professionName'] = current_profession.name
			res['data']['uploaderNickName'] = '未知'
			uploader = userInfo.objects.get(UserID=DATA[0]['fields']['UserID'],status=1)
			try:
				res['data']['uploaderNickName'] = uploader.nickName
			except userInfo.DoesNotExist:
				res['data']['uploaderNickName'] = '未知'

			res['data']['commentList'] = []
			comment_qset = comment.objects.filter(ResourceID=resource_id,status=1).order_by('-ctime')
			if len(comment_qset):
				COMMENT_DATA = json.loads(serializers.serialize("json", comment_qset))
				for current_comment in COMMENT_DATA:
					tmp = current_comment['fields']
					tmp['CommentID'] = current_comment['pk']
					tmp['commenterName'] = '未知用户'
					tmp['commenterAvatarUrl'] = ''
					user_id = current_comment['fields']['UserID']
					commenter = userInfo.objects.get(UserID=user_id,status=1)
					try:	
						tmp['commenterName'] = commenter.nickName
						tmp['commenterAvatarUrl'] = commenter.avatarUrl
					except userInfo.DoesNotExist:
						res['data']['uploaderNickName'] = '未知'

					res['data']['commentList'].append(tmp)
		else:
			res['data']['length'] = 0
			res['data']['ResourceID'] = resource_id

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 发表对资源的评价
@csrf_exempt
def makeComment(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		resource_id = int(request.POST['ResourceID'])
		user_id = int(request.POST['UserID'])
		comment_content = request.POST['content']
		comment_score = float(request.POST['score'])

		update = resource.objects.get(ResourceID=resource_id)
		if update.status == 0:
			res = {'code': -1, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		qset = comment.objects.filter(UserID=user_id,ResourceID=resource_id,status=1)
		if len(qset):
			res = {'code': -2, 'msg': '无法重复评论', 'data': {}}
			return HttpResponse(json.dumps(res))

		if serviceView.isLegalText(comment_content) == False:
			res = {'code': -3, 'msg': '评论内容违规', 'data': {}}
			return HttpResponse(json.dumps(res))

		insert = comment(UserID=user_id,ResourceID=resource_id,content=comment_content,score=comment_score)
		insert.save()

		new_avg_score = comment.objects.filter(ResourceID=resource_id,status=1).aggregate(avg=Avg("score")) 
		new_comment_count = comment.objects.filter(ResourceID=resource_id,status=1).count()

		update.avgScore = new_avg_score['avg']
		update.commentCount = new_comment_count				
		update.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 删除对资源的评价
@csrf_exempt
def deleteComment(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		comment_id = int(request.POST['CommentID'])

		update = comment.objects.get(CommentID=comment_id)
		if update.status == 0:
			res = {'code': -1, 'msg': '评论不存在', 'data': {}}
			return HttpResponse(json.dumps(res))

		resource_id = update.ResourceID
		resourceUpdate = resource.objects.get(ResourceID=resource_id)
		if resourceUpdate.status == 0:
			res = {'code': -2, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))

		update.status = 0
		update.save()
	
		new_comment_count = comment.objects.filter(ResourceID=resource_id,status=1).count()
		resourceUpdate.commentCount = new_comment_count	

		if new_comment_count > 0:
			new_avg_score = comment.objects.filter(ResourceID=resource_id,status=1).aggregate(avg=Avg("score")) 
			resourceUpdate.avgScore = new_avg_score['avg']
		else:
			resourceUpdate.avgScore = 0
					
		resourceUpdate.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 增加资源的访问次数
@csrf_exempt
def addResourceVisit(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		resource_id = int(request.POST['ResourceID'])
		
		update = resource.objects.get(ResourceID=resource_id)
		if update.status == 0:
			res = {'code': -1, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))

		update.visitCount += 1
		update.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 分类、分页搜索资源
@csrf_exempt
def getSelectedResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		search_title = request.POST['searchTitle'].replace(' ','')
		page_index = int(request.POST['pageIndex'])
		visit_ctrl = int(request.POST['visitCtrl'])
		order_rule = int(request.POST['orderRule'])
		profession_ids = json.loads(request.POST['ProfessionIDs'])

		# 排序规则定义
		order = '-ctime'
		if order_rule == 1:
			order = '-avgScore'
		if order_rule == 2:
			order = '-downloadCount'
		
		# 资源学科不限
		if (0 in profession_ids) or len(profession_ids) == 0:
			# 未设置搜索关键字，排序第二关键字始终是时间降序
			if search_title == '':
				qset = resource.objects.filter(visitCtrl__lte=visit_ctrl,status=1).order_by(order, '-ctime')
			else:
				qset = resource.objects.filter(visitCtrl__lte=visit_ctrl,status=1).filter(Q(title__contains=search_title) | Q(intro__contains=search_title)).order_by(order, '-ctime')
		
		# 资源列表包含指定的多个学科
		else:
			if search_title == '':
				qset = resource.objects.filter(ProfessionID__in=profession_ids,visitCtrl__lte=visit_ctrl,status=1).order_by(order, '-ctime')
			else:
				qset = resource.objects.filter(ProfessionID__in=profession_ids,visitCtrl__lte=visit_ctrl,status=1).filter(Q(title__contains=search_title) | Q(intro__contains=search_title)).order_by(order, '-ctime')
		length = 0
		if len(qset):
			res['data']['resourceList'] = []
			
			# 按4条/页对资源进行分页
			paginator = Paginator(qset, 4)

			# 防止越界
			if page_index < 1:
				page_index = 1
			if page_index > paginator.num_pages:
				page_index = paginator.num_pages
			
			# 获取前端指定的页面数据
			current_page = paginator.page(page_index)
			DATA = json.loads(serializers.serialize("json", current_page))
			for item in DATA:
				tmp = item['fields']
				tmp['ResourceID'] = item['pk']
				current_profession = profession.objects.get(ProfessionID=item['fields']['ProfessionID'])
				tmp['professionName'] = current_profession.name
				res['data']['resourceList'].append(tmp)
				length += 1
			res['data']['length'] = length

			# 因页面总数可能发生改变，前端请求的页码序号需要更新
			res['data']['totalPages'] = paginator.num_pages
			res['data']['pageNum'] = page_index
		else:
			res['data']['length'] = 0
			res['data']['totalPages'] = 1
			res['data']['pageNum'] = 1
	
	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))

# 举报资源
@csrf_exempt
def reportResource(request):
	request.encoding = 'utf-8'
	res = {'code': 0, 'msg': 'success', 'data':{}}
	try:
		resource_id = int(request.POST['ResourceID'])
		user_id = int(request.POST['UserID'])

		update = resource.objects.get(ResourceID=resource_id)
		if update.status == 0:
			res = {'code': -1, 'msg': '资源不存在', 'data': {}}
			return HttpResponse(json.dumps(res))
		
		qset = report.objects.filter(UserID=user_id,ResourceID=resource_id,status=1)
		if len(qset):
			res = {'code': -2, 'msg': '无法重复举报', 'data': {}}
			return HttpResponse(json.dumps(res))

		insert = report(UserID=user_id,ResourceID=resource_id)
		insert.save()

	except Exception as e:
		res = {'code': 500, 'msg': 'server error', 'data': {}}
		traceback.print_exc()

	return HttpResponse(json.dumps(res))