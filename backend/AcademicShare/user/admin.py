from django.contrib import admin
from user.models import userInfo, download, store

class userInfoAdmin(admin.ModelAdmin):
    list_display = ['UserID', 'nickName', 'account', 'password', 'studentID', 'studentName', 'avatarUrl', 'role', 'ctrl', 'status', 'ctime', 'mtime']
    ordering = ['ctime']

class downloadAdmin(admin.ModelAdmin):
    list_display = ['DownloadID', 'UserID', 'ResourceID', 'status', 'ctime', 'mtime']
    ordering = ['ctime']

class storeAdmin(admin.ModelAdmin):
    list_display = ['StoreID', 'UserID', 'ResourceID', 'status', 'ctime', 'mtime']
    ordering = ['ctime']

# Register your models here.
admin.site.register(userInfo, userInfoAdmin)
admin.site.register(download, downloadAdmin)
admin.site.register(store, storeAdmin)