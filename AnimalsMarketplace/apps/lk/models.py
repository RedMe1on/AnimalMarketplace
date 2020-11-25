from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class Profile(models.Model):
    """Профиль владельцев"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='catalogs/owner/img/', blank=True)
    email = models.EmailField(verbose_name='Почта', blank=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона', null=True, blank=True)
    pub_date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    pub_update = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Владелец'
        verbose_name_plural = 'Владельцы'


# Сигнал для присвоения новому User группы пользователя
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name=instance.username)
        group = Group.objects.get_or_create(name='Новые')
        instance.groups.add(group)
    else:
        instance.profile.save()
