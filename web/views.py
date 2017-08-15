import random

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
import django.forms as forms
from django.forms import ModelForm, HiddenInput
from .models import IndexPage, ContactPerson, ContactPhone, ContactEmail, JobCategory, ProjectPhoto, Project,\
                    ProjectComment, ProjectCommentatorSecret

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
        limit=21
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


@method_decorator(login_required, name='dispatch')
class PlainPage(View):

    def get(self, request, *args, **kwargs):
        page_code = kwargs.get('code', '')
        contact_info = get_base_contact()
        content = get_object_or_404(IndexPage, code=page_code)
        context = {'content': content}
        context.update(contact_info)
        return render(request, 'products.html', context=context)


@method_decorator(login_required, name='dispatch')
class ProjectView(View):

    def get(self, request, id, *args, **kwargs):
        contact_info = get_base_contact()
        obj = get_object_or_404(Project, pk=id)
        context = {'project': obj}
        context.update({'comments': ProjectComment.objects.filter(project=obj)})
        context.update(contact_info)
        return render(request, 'Project.html', context=context)

@method_decorator(login_required, name='dispatch')
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


class CommentForm(ModelForm):
    class Meta:
        model = ProjectComment
        fields = [
            #'project',
            'commentator_name',
            'text',
            #'creation_date',
            #'update_date',
            #'deleted'
            ]


class CommentView(View):

    def get(self, request, secret):
        sec = ProjectCommentatorSecret.objects.filter(secret=secret)
        if sec.count() < 1:
            return HttpResponse('Указан неверный код доступа. Получение данных невозможно.')
        project = sec[0].project
        print(project)
        comments = ProjectComment.objects.filter(project=project)
        print(comments)
        form = CommentForm(initial={'commentator_name': sec[0].commentator_name,
                                    'project':project})

        contact_info = get_base_contact()
        context = {'form': form, 'comments':comments, 'secret': secret}
        context.update(contact_info)

        return render(request, 'Comment.html', context=context)

    def post(self, request, secret):
        sec = ProjectCommentatorSecret.objects.filter(secret=secret)
        if sec.count() < 1:
            return HttpResponse('Указан неверный код доступа. Получение данных невозможно.')
        project = sec[0].project
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.secret = secret
            comment.save()
            return redirect(reverse('comment', args=[secret, ]))

        comments = ProjectComment.objects.filter(project=project)
        contact_info = get_base_contact()
        context = {'form': form, 'comments':comments}
        context.update(contact_info)
        return render(request, 'Comment.html', context=context)


class EditCommentForm(ModelForm):
    id = forms.IntegerField(widget=HiddenInput())
    class Meta:
        model = ProjectComment
        fields = ('id', 'project','secret',
            'commentator_name',
            'text',

        )
        widgets = {'project': HiddenInput(), 'secret':HiddenInput()}


class EditCommentView(View):

    def get(self, request, secret):
        sec = ProjectCommentatorSecret.objects.filter(secret=secret)
        if sec.count() < 1:
            return HttpResponse('Указан неверный код доступа. Получение данных невозможно.')
        project = sec[0].project
        instances_ordered = ProjectComment.objects.filter(secret=secret).order_by('-id')
        if instances_ordered.count() < 1:
            return redirect(reverse('comment', kwargs={'secret': secret}))
        last_comment = instances_ordered[0]
        form = EditCommentForm(instance=last_comment)
        comments = ProjectComment.objects.filter(project=project)
        contact_info = get_base_contact()
        context = {'form': form, 'comments':comments, 'secret': secret, 'id': last_comment.id}
        context.update(contact_info)
        return render(request, 'EditComment.html', context=context)

    def post(self, request, id, secret):
        sec = ProjectCommentatorSecret.objects.filter(secret=secret)
        if sec.count() < 1:
            return HttpResponse('Указан неверный код доступа. Получение данных невозможно.')
        project = sec[0].project
        instance = ProjectComment.objects.filter(pk=str(id))
        if instance.count() < 1:
            return redirect(reverse('comment', kwargs={'secret': secret}))
        form = EditCommentForm(request.POST, instance=instance[0])
        if form.is_valid():
            comment = form.save() #(commit=False)
            #comment.id = last_comment
            #comment.save()
            return redirect(reverse('project', kwargs={'id': project.id}) + '#comments_top')
        comments = ProjectComment.objects.filter(project=project)
        contact_info = get_base_contact()
        context = {'form': form, 'comments':comments, 'secret': secret, 'id': id}
        context.update(contact_info)
        return render(request, 'EditComment.html', context=context)

