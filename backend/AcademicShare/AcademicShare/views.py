# -*- coding: utf-8 -*-
from django.http import HttpResponse
from AcademicShare import settings
import os
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hello(request):
	return HttpResponse("Hello AcademicShare")
