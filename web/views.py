from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, View
from django.conf import settings
from .models import IndexPage

# Create your views here.

class Index(View):
    def get(self, request, *args, **kwargs):
        content = IndexPage.objects.get(code=settings.INDEXPAGE_CODE)
        return render(request, 'base.html', context={'content':content})
