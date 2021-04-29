from moderation import moderation
from moderation.moderator import GenericModerator
from moderation.signals import pre_moderation
from django.dispatch import receiver

from catalogs.models import Product, ProductImage


class ProductModerator(GenericModerator):
    notify_user = False
    auto_approve_for_groups = ['Модераторы']
    visible_until_rejected = True


moderation.register(Product, ProductModerator)
moderation.register(ProductImage, ProductModerator)


@receiver(pre_moderation, sender=Product)
def pre_moderation_product(sender, instance, status, **kwargs):
    if status == 0:
        instance.is_visible = False
    if status == 1:
        instance.is_visible = True
    instance.save()
