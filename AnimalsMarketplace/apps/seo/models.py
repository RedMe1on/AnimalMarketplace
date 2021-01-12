from django.core.validators import MaxLengthValidator
from django.db import models


# Create your models here.

class SeoModel(models.Model):
    seo_title = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)],
                                 verbose_name='Тайтл для поисковых систем')
    seo_description = models.CharField(max_length=300, blank=True, null=True, validators=[MaxLengthValidator(300)],
                                       verbose_name='Описание для поисковых систем')

    class Meta:
        abstract = True
