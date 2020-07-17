import re
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse
from pytils.translit import slugify
from django.core.exceptions import ValidationError


class Categories(MPTTModel):
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300, db_index=True)
    slug = models.SlugField(verbose_name='URL', max_length=150, unique=True, null=True, blank=True, allow_unicode=True)
    h1 = models.CharField(verbose_name='Заголовок h1', max_length=300, db_index=True)
    description = models.CharField(verbose_name='Мета-тег description', max_length=400)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE,
                            verbose_name='Родительская категория')
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.title

    def save(self):
        if self.slug is None:
            self.slug = slugify(self.h1)
        else:
            self.slug = slugify(self.slug)
        super().save()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['h1']


class Owner(models.Model):
    name = models.CharField(verbose_name='Владелец', max_length=50)
    email = models.EmailField(verbose_name='Почта', blank=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона', unique=True, null=False)
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'


class Product(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300, db_index=True)
    slug = models.SlugField(verbose_name='URL', max_length=150, unique=True, null=True, blank=True, allow_unicode=True)
    h1 = models.CharField(verbose_name='Заголовок h1', max_length=200, db_index=True)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.h1

    def get_absolute_url(self):
        return reverse('catalogs:ProductDetail', kwargs={'slug': self.slug})

    def save(self):
        if self.slug is None:
            self.slug = slugify(self.h1)
        else:
            self.slug = slugify(self.slug)
        super().save()

    class Meta:
        verbose_name = 'Карточка питомца'
        verbose_name_plural = 'Карточки питомца'
