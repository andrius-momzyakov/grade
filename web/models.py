import os
import urllib
import math
from PIL import Image
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class PhotoModel(models.Model):

    def gen_preview(self, type, custom_upload_to=''):
        """

        :param type: 'main' or 'preview' or 'thumbnail'
        :return:
        """
        base_image_dir, fname = os.path.split(self.image.url)
        os_full_path = os.path.join(settings.MEDIA_ROOT, custom_upload_to, urllib.parse.unquote(fname))
        base_image_dir, fname = os.path.split(os_full_path)
        # base_image_dir = os.path.dirname(base_image_dir)

        print('MEDIA_ROOT = "{}"'.format(settings.MEDIA_ROOT))
        print('image_url = "{}"'.format(self.image.url))
        print('base_image_dir = "{}"'.format(base_image_dir))
        print('full_path = {}'.format(os_full_path))

        width = 600
        preview_path = '/main/'
        if type == 'main':
            if hasattr(self.__class__, 'main_width'):
                width = self.__class__.main_width
            else:
                width = 600
            preview_path = '/main/'
        elif type == 'preview':
            if hasattr(self.__class__, 'preview_width'):
                width = self.__class__.preview_width
            else:
                width = 200
            preview_path = '/preview/'
        elif type == 'thumbnail':
            if hasattr(self.__class__, 'thumbnail_width'):
                width = self.__class__.thumbnail_width
            else:
                width = 100
            preview_path = '/thumbnails/'

        try:
            with Image.open(open(os_full_path, 'r+b')) as image:
                original_width = image.width
                original_height = image.height
                original_ratio = original_width / original_height
                height_byratio = round(width / original_ratio)
        except FileNotFoundError:
            print('ERROR: Can\'t open original: {}'.format(
                os_full_path))
            return

        try:
            with open(os_full_path, 'r+b') as f:
                with Image.open(f) as image:
                    cover = image.resize((width, height_byratio), Image.ANTIALIAS)
                    cover.save(base_image_dir + preview_path + fname, image.format)
        except FileNotFoundError:
            print('ERROR: Can\'t save preview: {}'.format(base_image_dir + '/main/' + fname))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if hasattr(self.__class__, 'custom_upload_to'):
            part1, fname = os.path.split(self.image.name)
            new_name = os.path.join(settings.MEDIA_ROOT, self.__class__.custom_upload_to, fname)
            old_name = os.path.join(settings.MEDIA_ROOT, self.image.name)
            try:
                os.rename(old_name, new_name)
                self.gen_previews(custom_upload_to=self.__class__.custom_upload_to)
                return
            except OSError:
                print('OS error occured while renaming {} to {}'.format(old_name, new_name))
                print('File haven\'t been moved, previews haven\'t been generated.')
                return
        self.gen_preview('main')
        self.gen_preview('preview')
        self.gen_preview('thumbnail')

    def get_preview_url(self):
        base_image_dir, fname = os.path.split(self.image.url)
        return base_image_dir + '/preview/' + fname

    def get_thumbnail_url(self):
        base_image_dir, fname = os.path.split(self.image.url)
        return base_image_dir + '/thumbnails/' + fname

    def get_main_url(self):
        base_image_dir, fname = os.path.split(self.image.url)
        return base_image_dir + '/main/' + fname

    def get_original_url(self):
        return self.image.url

    class Meta:
        abstract = True


class IndexPage(models.Model):
    code = models.CharField(max_length=100, verbose_name='Мнемокод для представления (уникальный)', unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок', null=True, blank=True)
    body = models.TextField(verbose_name='Содержание страницы')

    def __str__(self):
        return self.code + ' -> ' + self.title

    class Meta:
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория проектов'
        verbose_name_plural = 'Категории проектов'


class Segment(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сегмент рынка'
        verbose_name_plural = 'Сегменты рынка'


class Project(models.Model):
    code = models.CharField(max_length=100, verbose_name='Мнемокод для представления (уникальный)', unique=True)
    title = models.CharField(max_length=250, verbose_name='Заголовок страницы', null=True, blank=True)
    short_description = models.TextField(verbose_name='Краткое описание для списков (до 140 симв.)', max_length=140,
                                         null=True,
                                         blank=True)
    description = models.TextField(verbose_name='Содержание страницы')
    categories = models.ManyToManyField(Category, verbose_name='Категории')

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return self.code + ' -> ' + str(self.title)

    def get_url(self):
        return '/project/{}'.format(self.id)

    def get_thumbnail_url(self):
        prev = ProjectPhoto.objects.filter(project=self, is_thumb=True)
        if prev.count() > 0:
            return prev[0].get_thumbnail_url()
        else:
            return None

    def get_preview_url(self):
        prev = ProjectPhoto.objects.filter(project=self, is_thumb=True)
        if prev.count() > 0:
            return prev[0].get_preview_url()
        else:
            return None


class ProjectPhoto(PhotoModel):
    project = models.ForeignKey(Project, verbose_name='Объект')
    image = models.ImageField(verbose_name='Фото')
    alt_text = models.CharField(max_length=50, verbose_name='Альт. текст', null=True, blank=True)
    is_thumb = models.BooleanField(verbose_name='Использовать как иконку объекта', default=False)
    #is_preview = models.BooleanField(verbose_name='Использовать как превью объекта', default=False)

    class Meta:
        verbose_name = 'Фото объекта'
        verbose_name_plural = 'Фото объекта'

    def __str__(self):
        return self.project.code + ' -> ' + self.image.name


class JobCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Категория работ'
        verbose_name_plural = 'Категории работ'

    def __str__(self):
        return self.name


class Job(models.Model):
    jobcategory = models.ForeignKey(JobCategory, verbose_name='Категория работ')
    name = models.CharField(max_length=250, verbose_name='Название работы')
    unit = models.CharField(max_length=100, verbose_name='единица измерения')
    currency = models.CharField(max_length=10, verbose_name='Валюта (код)')
    price = models.IntegerField(verbose_name='Цена за ед.')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Вид Работы'
        verbose_name_plural = 'Виды Работ'
        unique_together=('jobcategory', 'name')

    def __str__(self):
        return self.jobcategory + ' -> ' + self.name


class Worker(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=50)
    surname = models.CharField(verbose_name='Фамилия', max_length=50)
    position = models.CharField(max_length=100, verbose_name='Специальность', null=True, blank=True)
    jobcategories = models.ManyToManyField('JobCategory', verbose_name='Услуги')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Мастер'
        verbose_name_plural = 'Мастера'

    def __str__(self):
        return self.name + ' ' + self.surname


class Contact(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя', null=True, blank=True)

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.name


class ContactPerson(models.Model):
    user = models.ForeignKey(User, verbose_name='Логин', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name='ФИО (Если не указан логин)', null=True, blank=True)
    photo = models.ImageField(verbose_name='Фото', null=True, blank=True)

    def __str__(self):
        return self.name


class ContactPhone(models.Model):
    person = models.ForeignKey(ContactPerson, verbose_name='Контактное лицо', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='Наименование телефона', null=True, blank=True)
    phone = models.CharField(max_length=30, verbose_name='Телефон:')
    place_on_header = models.BooleanField(verbose_name='Размещать в заголовке', default=False)

    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    def __str__(self):
        return self.person.name + ' -> ' + self.phone


class ContactEmail(models.Model):
    person = models.ForeignKey(ContactPerson, verbose_name='Контактное лицо', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='Наименование адреса', null=True, blank=True)
    email = models.EmailField(max_length=50, verbose_name='Электронная почта для связи')
    place_on_header = models.BooleanField(verbose_name='Размещать в заголовке', default=False)

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'

    def __str__(self):
        return self.person.name + ' -> ' + self.email
