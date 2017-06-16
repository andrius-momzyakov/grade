from django.conf.urls import url, include
from django.contrib import admin
from . import views
from ckeditor_uploader import urls as ck_urls

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^products/$', views.Products.as_view(), name='products')
]