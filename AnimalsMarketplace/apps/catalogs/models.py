from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField
from django.shortcuts import reverse
from pytils.translit import slugify


class Categories(MPTTModel):
    name = models.CharField(verbose_name='Название категории', max_length=150)
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300, db_index=True, blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=150, unique=True, blank=True, allow_unicode=True)
    h1 = models.CharField(verbose_name='Заголовок h1', max_length=300, db_index=True)
    description = models.CharField(verbose_name='Мета-тег description', max_length=300, blank=True)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE,
                            verbose_name='Родительская категория')
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.h1)
        else:
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['h1']


class Owner(models.Model):
    name = models.CharField(verbose_name='Владелец', max_length=50)
    image = models.ImageField(verbose_name='Изображение', upload_to='catalogs/owner/img/', blank=True)
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
    name = models.CharField(verbose_name='Название товара', max_length=150)
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300, db_index=True, blank=True)
    h1 = models.CharField(verbose_name='Заголовок h1', max_length=200, db_index=True)
    slug = models.SlugField(verbose_name='URL', max_length=150, unique=True, blank=True, allow_unicode=True)
    description = models.CharField(verbose_name='Мета-тег description', max_length=300, blank=True)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    image = models.ImageField(verbose_name='Главная фотография', upload_to='catalogs/product/img', blank=True)
    draft = models.BooleanField(verbose_name='Черновик', help_text='Черновики не отображаются на сайте')
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name='Владелец')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Родительская категория')
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.h1

    def get_absolute_url(self):
        return reverse('catalogs:product_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('catalogs:product_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('catalogs:product_delete', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.h1)
        else:
            self.slug = slugify(self.slug)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Карточка питомца'
        verbose_name_plural = 'Карточки питомца'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Дополнительные фотографии', upload_to='catalogs/product/img')

    class Meta:
        verbose_name = 'Дополнительные фотографии'
        verbose_name_plural = 'Дополнительные фотографии'
