from moderation import moderation
from moderation.moderator import GenericModerator

from lk.models import Profile


class UserProfileModerator(GenericModerator):
    notify_user = False
    # auto_approve_for_superusers = True


# moderation.register(Profile, UserProfileModerator)
