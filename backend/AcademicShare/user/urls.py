from django.urls import path, re_path, include

from user import views

urlpatterns = [
    re_path(r'^hello$', views.hello),
    re_path(r'^getAllUserInfo$', views.getAllUserInfo),
    re_path(r'^getAllDownload$', views.getAllDownload),
    re_path(r'^getAllStore$', views.getAllStore),
    re_path(r'^register$', views.register),
    re_path(r'^login$', views.login),
    re_path(r'^authentication$', views.authentication),
    re_path(r'^modifyPassword$', views.modifyPassword),
    re_path(r'^modifyNickname$', views.modifyNickname),
    re_path(r'^storeResource$', views.storeResource),
    re_path(r'^cancelStoreResource$', views.cancelStoreResource),
    re_path(r'^getStoreResource$', views.getStoreResource),
    re_path(r'^downloadResource$', views.downloadResource),
    re_path(r'^getDownloadResource$', views.getDownloadResource),
    re_path(r'^getUploadResource$', views.getUploadResource),
    re_path(r'^cancelUploadResource$', views.cancelUploadResource),
]