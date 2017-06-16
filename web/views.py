from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, View
from django.conf import settings
from .models import IndexPage, Contact, JobCategory

# Create your views here.

def get_base_contact():
    try:
        contact = Contact.objects.all()[0]
    except IndexError:
        contact = None
    if contact:
        try:
            phone = contact.contactphone_set.all()[0].phone
        except IndexError:
            phone = None
        try:
            email = contact.contactemail_set.all()[0].email
        except IndexError:
            email = None
        return {'header_phone':phone, 'header_email': email}
    return {}


class Index(View):

    def get(self, request, *args, **kwargs):
        contact_info = get_base_contact()
        # return HttpResponse(contact_info['header_email'])
        content = IndexPage.objects.get(code=settings.INDEXPAGE_CODE)
        context = {'content':content}
        context.update(contact_info)
        return render(request, 'index.html', context=context)


class Products(View):

    def get(self, request, *args, **kwargs):
        qs = JobCategory.objects.all()
        return HttpResponse('Products page')