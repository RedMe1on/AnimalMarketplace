from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from catalogs.models import Product, Categories


class ProfileViewsTestCase(TestCase):
    """Test case for profile view"""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestUser1', password='TestUser1')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('lk:profile'))
        self.assertRedirects(resp, f'/accounts/login/?next={reverse("lk:profile")}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:profile'))

        # Checking that the user is logged in
        self.assertEqual(str(resp.context['user']), 'TestUser1')

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lk/profile.html')


class ProfileEditViewsTestCase(TestCase):
    """Test case for profile view"""

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='TestUser1', password='TestUser1')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('lk:edit_profile'))
        self.assertRedirects(resp, f'/accounts/login/?next={reverse("lk:edit_profile")}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:edit_profile'))

        # Checking that the user is logged in
        self.assertEqual(str(resp.context['user']), 'TestUser1')

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lk/profile_update.html')

    def test_success_url_form_valid_renewal_profile(self):
        self.client.login(username='TestUser1', password='TestUser1')
        form_data = {
            'name': 'TestUser1',
            'phone_number_ads': '+7 (999) 999-65-65',
        }
        resp = self.client.post(reverse('lk:edit_profile'), form_data)
        self.assertRedirects(resp, reverse("lk:profile"))

    def test_form_invalid_renewal_email(self):
        self.client.login(username='TestUser1', password='TestUser1')
        form_data_invalid = {
            'name': 'TestUser1',
            'phone_number_ads': '+7 (999) 999-65-65',
            'email': 'dsadsadsa'
        }
        resp = self.client.post(reverse('lk:edit_profile'), form_data_invalid)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'email',
                             'Введите правильный адрес электронной почты в формате xxxxx@xxxxx.xx')

    def test_form_invalid_renewal_phone_number_ads(self):
        self.client.login(username='TestUser1', password='TestUser1')
        form_data_invalid = {
            'name': 'TestUser1',
            'phone_number_ads': '+7(999)9996565invalid',
            'email': 'dsadsadsa'
        }
        resp = self.client.post(reverse('lk:edit_profile'), form_data_invalid)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'phone_number_ads',
                             'Введите телефон в формате +7 (XXX) XXX-XX-XX')

    def test_form_invalid_renewal_phone_number(self):
        self.client.login(username='TestUser1', password='TestUser1')
        form_data_invalid = {
            'name': 'TestUser1',
            'phone_number_ads': '+79999999999',
            'email': 'dsadsadsa',
            'phone_number': '+7(999)9996565invalid'
        }
        resp = self.client.post(reverse('lk:edit_profile'), form_data_invalid)
        self.assertEqual(resp.status_code, 200)
        self.assertFormError(resp, 'form', 'phone_number',
                             'Введите телефон в формате +7 (XXX) XXX-XX-XX')


class ProductDeleteViewTestCase(TestCase):
    """Test case for profile view"""

    def setUp(self) -> None:
        self.test_user_1 = User.objects.create_user(username='TestUser1', password='TestUser1')
        self.test_user_2 = User.objects.create_user(username='TestUser2', password='TestUser2')

        self.category = Categories.objects.create(name='TestCategory1', h1='TestCategory1_H1')

        number_product = 30
        for product in range(number_product):
            if product < 15:
                Product.objects.create(name=f'TestProduct{product}', user=self.test_user_1, category=self.category)
            else:
                Product.objects.create(name=f'TestProduct{product}', user=self.test_user_2, category=self.category)

        self.product = Product.objects.get(name='TestProduct1')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.post(reverse('lk:product_delete', kwargs={'pk': self.product.pk}))
        self.assertRedirects(resp,
                             f'/accounts/login/?next={reverse("lk:product_delete", kwargs={"pk": self.product.pk})}')

    def test_success_url_form_valid_renewal_profile(self):
        product = Product.objects.create(user=self.test_user_1, category=self.category)
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.post(reverse('lk:product_delete', kwargs={'pk': product.pk}))
        self.assertRedirects(resp, reverse('lk:product_list'))

    def test_delete_objects(self):
        product = Product.objects.create(user=self.test_user_1, category=self.category)
        pk = product.pk
        self.client.login(username='TestUser1', password='TestUser1')
        self.client.post(reverse('lk:product_delete', kwargs={'pk': pk}))
        #TODO незакончен тест - нужно завершить
        self.assertEqual(get_object_or_404(Product, pk=pk), Http404('No Product matches the given query.'))
