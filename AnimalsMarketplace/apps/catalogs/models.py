from django.db import models
from datetime import datetime


class Categories(models.Model):
    categories_title = models.CharField('Мета-тег Title', max_length=300)
    categories_h1 = models.CharField('Заголовок h1', max_length=300)
    categories_description = models.CharField('Мета-тег description', max_length=400)
    categories_text = models.TextField('Описание')
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.categories_title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Owner(models.Model):
    owner_name = models.CharField('Владелец', max_length=50)
    owner_email = models.CharField('Почта', max_length=200)
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.owner_name

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'


class Product(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    product_h1 = models.CharField('Заголовок h1', max_length=200)
    product_text = models.TextField('Описание')
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.product_h1

    class Meta:
        verbose_name = 'Карточка питомца'
        verbose_name_plural = 'Карточки питомца'
