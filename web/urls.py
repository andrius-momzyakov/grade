from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from ckeditor_uploader import urls as ck_urls

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^products/$', views.Products.as_view(), name='products'),
    url(r'^project/(?P<id>\w+)$', views.ProjectView.as_view(), name='project'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)