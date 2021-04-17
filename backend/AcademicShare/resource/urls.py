from django.urls import path, re_path, include

from resource import views

urlpatterns = [
    re_path(r'^hello$', views.hello),
    re_path(r'^getAllResource$', views.getAllResource),
    re_path(r'^getAllReport$', views.getAllReport),
    re_path(r'^uploadFile$', views.uploadFile), 
    re_path(r'^getResouceDetailByID$', views.getResouceDetailByID),
    re_path(r'^makeComment$', views.makeComment),
    re_path(r'^deleteComment$', views.deleteComment),
    re_path(r'^addResourceVisit$', views.addResourceVisit),
    re_path(r'^getSelectedResource$', views.getSelectedResource),
    re_path(r'^reportResource$', views.reportResource),
]