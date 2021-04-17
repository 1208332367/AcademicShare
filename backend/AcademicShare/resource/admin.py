from django.contrib import admin
from resource.models import resource, comment, report, wx_token

class resourceAdmin(admin.ModelAdmin):
    list_display = ['ResourceID', 'title', 'fileSize', 'localUrl', 'ProfessionID', 'visitCtrl', 'intro', 'avgScore', 'UserID', 'visitCount', 'storeCount', 'downloadCount', 'commentCount', 'status', 'ctime', 'mtime']
    ordering = ['ctime']

class commentAdmin(admin.ModelAdmin):
    list_display = ['CommentID', 'UserID', 'ResourceID', 'content', 'score', 'status', 'ctime', 'mtime']
    ordering = ['ctime']

class reportAdmin(admin.ModelAdmin):
    list_display = ['ReportID', 'UserID', 'ResourceID', 'status', 'ctime', 'mtime']
    ordering = ['ctime']

class tokenAdmin(admin.ModelAdmin):
    list_display = ['access_token', 'update_time', 'status']

# Register your models here.
admin.site.register(resource, resourceAdmin)
admin.site.register(comment, commentAdmin)
admin.site.register(report, reportAdmin)
admin.site.register(wx_token, tokenAdmin)