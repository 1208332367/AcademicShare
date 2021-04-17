from django.urls import path, re_path, include

from profession import views

urlpatterns = [
    re_path(r'^hello$', views.hello),
    re_path(r'^insertProfession$', views.insertProfession),
    re_path(r'^listProfession$', views.listProfession),
]