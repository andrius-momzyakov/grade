from django.db import models

# Create your models here.

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
    description = models.TextField(verbose_name='Содержание страницы')
    categories = models.ManyToManyField(Category, verbose_name='Категории')

    class Meta:
        verbose_name = 'Объект для портфолио'
        verbose_name_plural = 'Объекты для портфолио'

    def __str__(self):
        return self.code + ' -> ' + self.title


class ProjectPhoto(models.Model):
    project = models.ForeignKey(Project, verbose_name='Объект')
    image = models.ImageField(verbose_name='Фото')
    alt_text = models.CharField(max_length=50, verbose_name='Альт. текст', null=True, blank=True)

    class Meta:
        verbose_name = 'Фото объекта'
        verbose_name_plural = 'Фото объекта'

    def __str__(self):
        return self.project + ' -> ' + self.image.name


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