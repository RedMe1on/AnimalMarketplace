from django.db import models
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey


class Categories(MPTTModel):
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300)
    slug = models.SlugField(verbose_name='URL', max_length=150, unique=True)
    h1 = models.CharField(verbose_name='Заголовок h1', max_length=300)
    description = models.CharField(verbose_name='Мета-тег description', max_length=400)
    text = models.TextField(verbose_name='Описание')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE,
                            verbose_name='Родительская категория')
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['h1']


class Owner(models.Model):
    name = models.CharField('Владелец', max_length=50)
    email = models.CharField('Почта', max_length=200)
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'


class Product(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300)
    slug = models.SlugField(verbose_name='URL', max_length=150, unique=True)
    h1 = models.CharField('Заголовок h1', max_length=200)
    text = models.TextField('Описание')
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.h1

    class Meta:
        verbose_name = 'Карточка питомца'
        verbose_name_plural = 'Карточки питомца'
