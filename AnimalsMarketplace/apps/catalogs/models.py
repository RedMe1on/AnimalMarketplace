from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse
from pytils.translit import slugify
from django.utils.translation import gettext_lazy as _


class Categories(MPTTModel):
    """Модель для хранения категорий"""
    name = models.CharField(verbose_name='Название категории', max_length=150)
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300, db_index=True, blank=True)
    slug = models.SlugField(verbose_name='URL', max_length=150, unique=True, blank=True, allow_unicode=True)
    h1 = models.CharField(verbose_name='Заголовок h1', max_length=300, db_index=True)
    description = models.CharField(verbose_name='Мета-тег description', max_length=300, blank=True)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    image = models.ImageField(upload_to='catalogs/categories/img', verbose_name='Фотография', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE,
                            verbose_name='Родительская категория')
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.h1)
        else:
            self.slug = slugify(self.slug)
        # обработка неуникального slug
        while True:
            try:
                self.validate_unique()
                break
            except ValidationError:
                self.slug += '-copy'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalogs:categories_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    class MPTTMeta:
        order_insertion_by = ['h1']


class BreedType(models.Model):
    """Модель для хранения типов пород"""
    name = models.CharField(verbose_name='Название породы', max_length=200)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, verbose_name='Вид животного', null=True,
                                 related_name='breed_types')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид породы'
        verbose_name_plural = 'Виды пород'


class Product(models.Model):
    """Модель для хранения объявлений"""

    class SexChoices(models.TextChoices):
        UNKNOWN = 'Неизвество', _('Неизвество')
        BOY = 'Мальчик', _('Мальчик')
        GIRL = 'Девочка', _('Девочка')

    class BreedChoices(models.TextChoices):
        UNKNOWN = 'Неизвество', _('Неизвество')
        THOROUGHBRED = 'Породистый', _('Породистый')
        CROSSBRED = 'Метис', _('Метис')
        PUREBRED = 'Беспородный', _('Беспородный')

    name = models.CharField(verbose_name='Заголовок объявления', max_length=150, db_index=True)
    title = models.CharField(verbose_name='Мета-тег Title', max_length=300, db_index=True, blank=True)
    description = models.CharField(verbose_name='Мета-тег description', max_length=300, blank=True)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    sex = models.CharField(verbose_name='Пол питомца', max_length=10, choices=SexChoices.choices)
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    age_type = models.BooleanField(verbose_name='Указать возраст в месяцах', default=False, blank=True)
    age = models.IntegerField(verbose_name='Возраст', blank=True, null=True)
    breed = models.CharField(verbose_name='Порода', max_length=12, choices=BreedChoices.choices,
                             default=BreedChoices.UNKNOWN, blank=True)
    breed_type = models.ForeignKey(BreedType, on_delete=models.SET_NULL, null=True, verbose_name='Вид породы',
                                   blank=True)
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True, default=0)
    draft = models.BooleanField(verbose_name='Черновик', help_text='Черновики не отображаются на сайте', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', null=True)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True,
                                 verbose_name='Родительская категория')
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogs:product_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('lk:product_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('lk:product_delete', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Карточка питомца'
        verbose_name_plural = 'Карточки питомца'


class ProductImage(models.Model):
    """Модель для хранения изображений объявлений"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_img')
    image = models.ImageField(verbose_name='Дополнительная фотография', upload_to='catalogs/product/img', blank=True,
                              null=True)

    class Meta:
        verbose_name = 'Дополнительные фотографии'
        verbose_name_plural = 'Дополнительные фотографии'
        ordering = ['id']


class ReportModel(models.Model):
    """Модель для хранения жалоб"""

    class CauseChoices(models.TextChoices):
        STRANGER = 'Указан чужой номер телефона', _('Указан чужой номер телефона')
        DISABLED = 'Номер отключен', _('Номер отключен')
        NOT_RELEVANT = 'Неактуально', _('Неактуально')
        OTHER = 'Другая причина (укажите в комментарии)', _('Другая причина (укажите в комментарии)')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Объявление')
    comment = models.CharField(max_length=300, verbose_name='Комментарий', blank=True)
    cause = models.CharField(max_length=100, verbose_name='Причина', choices=CauseChoices.choices)

    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
