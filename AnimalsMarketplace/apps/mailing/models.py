from django.db import models


class Mailing(models.Model):
    """Подписаться на рассылку"""
    email = models.EmailField(unique=True, verbose_name='E-mail')
    date = models.DateField(auto_now_add=True, verbose_name='Дата подписки')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Адрес для рассылки'
        verbose_name_plural = 'Адреса для рассылки'



