from moderation import moderation
from moderation.moderator import GenericModerator

from lk.models import Profile
from catalogs.models import Product


class UserProductModerator(GenericModerator):
    notify_user = False
    auto_approve_for_groups = ['Модераторы']


moderation.register(Product)
