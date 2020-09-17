from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Profile(models.Model):
    """Профиль владельцев"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(verbose_name='Имя', max_length=50)
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