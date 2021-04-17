from django.db import models
from django.utils import timezone

class profession(models.Model):
    ProfessionID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    ctime = models.DateTimeField(default=timezone.now)
    mtime = models.DateTimeField(auto_now=True)