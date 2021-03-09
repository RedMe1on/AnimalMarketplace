from django.contrib.auth.models import User, Group
from django.test import TestCase

from lk.models import Profile


class ProfileModelTestCase(TestCase):
    """Test case for profile model"""

    def setUp(self):
        self.user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')


    # def test_signal_post_save_user(self):
    #     self.assertTrue(Profile.objects.get(name=self.user.username, user=self.user))

