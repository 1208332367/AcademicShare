from django.db import models
from django.utils import timezone

class userInfo(models.Model):
    UserID = models.AutoField(primary_key=True)
    nickName = models.CharField(max_length=100)
    account = models.CharField(max_length=100)
    password = models.CharField(max_length=500)
    studentID = models.CharField(max_length=50,blank=True,null=True)
    studentName = models.CharField(max_length=100,blank=True,null=True)
    avatarUrl = models.CharField(max_length=500,blank=True,default="")
    role = models.IntegerField(default=1)
    ctrl = models.IntegerField(default=7)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default=timezone.now)
    mtime = models.DateTimeField(auto_now=True)

class download(models.Model):
    DownloadID = models.AutoField(primary_key=True)
    UserID = models.IntegerField(default=0)
    ResourceID = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default=timezone.now)
    mtime = models.DateTimeField(auto_now=True)

class store(models.Model):
    StoreID = models.AutoField(primary_key=True)
    UserID = models.IntegerField(default=0)
    ResourceID = models.IntegerField(default=0)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default=timezone.now)
    mtime = models.DateTimeField(auto_now=True)