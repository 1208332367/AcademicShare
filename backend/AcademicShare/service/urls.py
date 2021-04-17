from django.conf.urls import url
from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r'^resource/', include('resource.urls')),
    re_path(r'^user/', include('user.urls')),
    re_path(r'^profession/', include('profession.urls')),
]

