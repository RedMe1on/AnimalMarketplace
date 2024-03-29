from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
from blog.models import PublicationModel


class Profile(PublicationModel):
    """Профиль владельцев"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=50, blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='catalogs/owner/img/', blank=True)
    email = models.EmailField(verbose_name='Почта', blank=True)
    phone_number = PhoneNumberField(verbose_name='Номер телефона для связи', null=True, blank=True)
    phone_number_ads = PhoneNumberField(verbose_name='Номер телефона для обявлений',
                                        help_text='Этот номер телефона будет отображаться на ваших объявлениях')

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
        group, create_group = Group.objects.get_or_create(name='Новые')
        instance.groups.add(group)
