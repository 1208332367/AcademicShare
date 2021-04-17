from django.db import models
from django.utils import timezone

class resource(models.Model):
    ResourceID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    fileSize = models.FloatField(default=0.0)  #KB
    localUrl = models.CharField(max_length=500)
    ProfessionID = models.IntegerField(default=0)
    visitCtrl = models.IntegerField(default=1)
    intro = models.CharField(max_length=500)
    avgScore = models.FloatField(default=0.0)
    UserID = models.IntegerField(default=0)
    visitCount = models.IntegerField(default=0)
    storeCount = models.IntegerField(default=0)
    downloadCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default=timezone.now)
    mtime = models.DateTimeField(auto_now=True)

class comment(models.Model):
    CommentID = models.AutoField(primary_key=True)
    UserID = models.IntegerField(default=0)
    ResourceID = models.IntegerField(default=0)
    content = models.CharField(max_length=500)
    score = models.FloatField(default=0.0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default=timezone.now)
    mtime = models.DateTimeField(auto_now=True)

class report(models.Model):
    ReportID = models.AutoField(primary_key=True)
    ResourceID = models.IntegerField(default=0)
    UserID = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default=timezone.now)
    mtime = models.DateTimeField(auto_now=True) 

class wx_token(models.Model):
    access_token = models.CharField(max_length=1000,default='')
    update_time = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
