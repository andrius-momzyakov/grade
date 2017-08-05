import random

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, View
from django.conf import settings
from .models import IndexPage, ContactPerson, ContactPhone, ContactEmail, JobCategory, ProjectPhoto, Project

# Create your views here.


def get_base_contact():
    try:
        phone = ', '.join([cp.phone for cp in ContactPhone.objects.filter(place_on_header=True)])
    except IndexError:
        phone = None
    try:
        email = ', '.join([cp.email for cp in ContactEmail.objects.filter(place_on_header=True)])
    except:
        email = None
    return {'header_phone': phone, 'header_email': email}


class Index(View):

    def get(self, request, *args, **kwargs):
        contact_info = get_base_contact()
        # return HttpResponse(contact_info['header_email'])

        content = IndexPage.objects.get(code=settings.INDEXPAGE_CODE)
        context = {'content': content}
        context.update(contact_info)
        # фото объектов
        cnt = ProjectPhoto.objects.count()
        photos = []
        rownums = []
        limit=12
        if cnt < limit:
            limit = cnt
        for i in range(limit):
            while True:
                rn = random.randint(0, cnt-1)
                if rn in rownums:
                    continue
                rownums.append(rn)
                photos.append(ProjectPhoto.objects.all()[rn])
                break
        print(photos)
        context.update({'photos': photos})
        return render(request, 'index.html', context=context)


class Products(View):
    def get(self, request, *args, **kwargs):
        contact_info = get_base_contact()
        content = IndexPage.objects.get(code=settings.PRODUCTS_CODE)
        context = {'content': content}
        context.update(contact_info)
        return render(request, 'products.html', context=context)


class ProjectView(View):

    def get(self, request, id, *args, **kwargs):
        contact_info = get_base_contact()
        obj = get_object_or_404(Project, pk=id)
        context = {'project': obj}
        context.update(contact_info)
        return render(request, 'Project.html', context=context)

class ProjectListView(View):

    def get(self, request, *args, **kwargs):
        contact_info = get_base_contact()
        list_content = Project.objects.all()
        context = {'list': list_content}
        context.update(contact_info)
        return render(request, 'Projects.html', context=context)



class ContactView(View):

    def get(self, request, *args, **kwargs):
        qs = ContactPerson.objects.all()
        contact_info = get_base_contact()
        context = {'contacts': qs}
        context.update(contact_info)
        return render(request, 'Contact.html', context=context)
