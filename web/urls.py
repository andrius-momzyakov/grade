from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from . import views
from ckeditor_uploader import urls as ck_urls

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^products/$', views.PlainPage.as_view(), {'code': settings.PRODUCTS_CODE}, name='products'),
    url(r'^project/(?P<id>\w+)$', views.ProjectView.as_view(), name='project'),
    url(r'^contact/$', views.ContactView.as_view(), name='contact'),
    url(r'^portfolio/', views.ProjectListView.as_view(), name='project_list'),
    url('^accounts/', include('django.contrib.auth.urls')),
    url(r'^license/$', views.PlainPage.as_view(), {'code': settings.LICENSE_CODE}, name='license'),
    url(r'^comment/(?P<secret>\w+)$', views.CommentView.as_view(), name='comment'),
    url(r'^comment/edit/(?P<secret>\w+)$', views.EditCommentView.as_view(), name='editcomment'),
    url(r'^comment/edit/(?P<id>\d+)/(?P<secret>\w+)$', views.EditCommentView.as_view(), name='editcomment')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)