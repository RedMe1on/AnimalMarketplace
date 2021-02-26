from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from pytils.translit import slugify
from seo.models import SeoModel


class PublicationModel(models.Model):
    pub_update = models.DateField(auto_now=True, verbose_name='Дата обновления публикации')
    pub_date = models.DateField(auto_now_add=True, verbose_name='Дата создания публикации')

    class Meta:
        abstract = True


class Categories(SeoModel, PublicationModel):
    name = models.CharField(max_length=200, verbose_name='Название категории')
    slug = models.SlugField(allow_unicode=True, unique=True, blank=True, verbose_name='URL', max_length=150)
    image = models.ImageField(upload_to='blog/categories/img', blank=True, verbose_name='Изображение')
    short_text = models.CharField(max_length=40, verbose_name='Короткое описание', blank=True)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    priority = models.IntegerField(verbose_name='Приоритет',
                                   help_text='Приоритет на вывод в топ категорий на главной блога (больше - лучше)',
                                   blank=True, null=True, default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)
        # обработка неуникального slug
        try:
            self.validate_unique()
        except ValidationError:
            self.slug += '-copy'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:categories_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class BlogTags(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название тега')
    slug = models.SlugField(verbose_name='URL', max_length=150, allow_unicode=True, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)
        # обработка неуникального slug
        try:
            self.validate_unique()
        except ValidationError:
            self.slug += '-copy'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Post(SeoModel, PublicationModel):
    name = models.CharField(max_length=200, verbose_name='Название публикации')
    slug = models.SlugField(verbose_name='URL', max_length=150, allow_unicode=True, blank=True, unique=True)
    text = models.TextField(verbose_name='Описание', blank=True, db_index=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='blog/post/img', blank=True)
    views = models.PositiveIntegerField(verbose_name='Количество просмотров', default=0, blank=True)
    draft = models.BooleanField(verbose_name='Черновик', help_text='Не отображается на сайте')
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True,
                                 verbose_name='Родительская категория')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    tags = models.ManyToManyField(BlogTags, verbose_name='Теги', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.name)
        else:
            self.slug = slugify(self.slug)
        # обработка неуникального slug
        try:
            self.validate_unique()
        except ValidationError:
            self.slug += '-copy'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


