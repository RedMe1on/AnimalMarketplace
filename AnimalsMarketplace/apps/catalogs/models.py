from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse
from pytils.translit import slugify
from django.utils.translation import gettext_lazy as _


# class GetAbsoluteUrlMixin(models.Model):
#     slug = models.SlugField(verbose_name='URL', max_length=150, unique=True, blank=True, allow_unicode=True)
#     url_name = None
#
#     def get_absolute_url(self):
#         return reverse(self.url_name, kwargs={'slug': self.slug})
#
#         class Meta:
#             abstract = True


class Categories(MPTTModel):
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
        try:
            self.validate_unique()
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


class Product(models.Model):
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
    sex = models.CharField(verbose_name='Пол питомца', max_length=10, choices=SexChoices.choices, default='Любой')
    birthday = models.DateField(verbose_name='Дата рождения', blank=True, null=True)
    age_type = models.BooleanField(verbose_name='Указать возраст в месяцах', default=False, blank=True)
    age = models.IntegerField(verbose_name='Возраст', blank=True, null=True)
    breed = models.CharField(verbose_name='Порода', max_length=12, choices=BreedChoices.choices,
                             default='Неизвестно')
    breed_type = models.CharField(verbose_name='Вид породы', max_length=200, blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name='Цена', blank=True, default=0)
    image = models.ImageField(verbose_name='Главная фотография', upload_to='catalogs/product/img', blank=True)
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Дополнительные фотографии', upload_to='catalogs/product/img')

    class Meta:
        verbose_name = 'Дополнительные фотографии'
        verbose_name_plural = 'Дополнительные фотографии'


# class BreedType(models.Model):
#     category = models.ForeignKey(Categories, on_delete=models.SET_NULL, verbose_name='Категория породы')
#     name = models.CharField(verbose_name='Название породы', max_length=200)


class RatingProduct(models.Model):
    """Модель для хранения рейтинга товаров"""

    class Star(models.IntegerChoices):
        VERY_BAD = 1, _('Очень плохо')
        BAD = 2, _('Плохо')
        NOT_BAD = 3, _('Неплохо')
        GOOD = 4, _('Хорошо')
        VERY_GOOD = 5, _('Очень хорошо')

    ip = models.CharField(verbose_name='IP', max_length=30)
    rating = models.IntegerField(choices=Star.choices, verbose_name='Рейтинг')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Питомец')

    def __str__(self):
        return f'{self.rating} - {self.product}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
