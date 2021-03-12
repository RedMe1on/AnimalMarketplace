from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from catalogs.models import Product, Categories

from lk.models import Profile


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

    def setUp(self) -> None:
        self.profile = Profile.objects.get(name='TestUser1')

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

    def test_update_profile(self):
        self.client.login(username='TestUser1', password='TestUser1')
        form_data = {
            'name': 'TestUser12',
            'phone_number_ads': '+7 (999) 999-65-65',
        }
        self.client.post(reverse('lk:edit_profile'), form_data)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.name, 'TestUser12')

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


class ProductListViewTestCase(TestCase):
    """Test case for profile view"""

    def setUp(self) -> None:
        self.test_user_1 = User.objects.create_user(username='TestUser1', password='TestUser1')
        self.test_user_2 = User.objects.create_user(username='TestUser2', password='TestUser2')

        self.category = Categories.objects.create(name='TestCategory1', h1='TestCategory1_H1')

        number_product = 30
        for product_number in range(number_product):
            if product_number < 15:
                Product.objects.create(name=f'TestProduct{product_number}', user=self.test_user_1,
                                       category=self.category)
            else:
                Product.objects.create(name=f'TestProduct{product_number}', user=self.test_user_2,
                                       category=self.category)

        self.product = Product.objects.get(name='TestProduct1')
        self.product_user_2 = Product.objects.get(name='TestProduct20')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.post(reverse('lk:product_list'))
        self.assertRedirects(resp,
                             f'/accounts/login/?next={reverse("lk:product_list")}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:product_list'))

        # Checking that the user is logged in
        self.assertEqual(str(resp.context['user']), 'TestUser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lk/product_list.html')

    def test_pagination_is_ten(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['product_list']) == 10)

    def test_lists_all_product(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:product_list') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['product_list']) == 5)

    def test_all_product_belong_user(self):
        self.client.login(username='TestUser2', password='TestUser2')
        resp = self.client.get(reverse('lk:product_list'))
        for product in resp.context['product_list']:
            self.assertEqual(product.user, self.test_user_2)


class ProductDeleteViewTestCase(TestCase):
    """Test case for profile view"""

    def setUp(self) -> None:
        self.test_user_1 = User.objects.create_user(username='TestUser1', password='TestUser1')
        self.test_user_2 = User.objects.create_user(username='TestUser2', password='TestUser2')

        self.category = Categories.objects.create(name='TestCategory1', h1='TestCategory1_H1')

        number_product = 30
        for product_number in range(number_product):
            if product_number < 15:
                Product.objects.create(name=f'TestProduct{product_number}', user=self.test_user_1,
                                       category=self.category)
            else:
                Product.objects.create(name=f'TestProduct{product_number}', user=self.test_user_2,
                                       category=self.category)

        self.product = Product.objects.get(name='TestProduct1')
        self.product_user_2 = Product.objects.get(name='TestProduct20')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('lk:product_delete', kwargs={'pk': self.product.pk}))
        self.assertRedirects(resp,
                             f'/accounts/login/?next={reverse("lk:product_delete", kwargs={"pk": self.product.pk})}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:product_delete', kwargs={'pk': self.product.pk}))

        # Checking that the user is logged in
        self.assertEqual(str(resp.context['user']), 'TestUser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lk/product_delete.html')

    def test_success_url_form_valid_delete_product(self):
        self.client.login(username='TestUser2', password='TestUser2')
        resp = self.client.post(reverse('lk:product_delete', kwargs={'pk': self.product_user_2.pk}))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('lk:product_list'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.post(reverse('lk:product_delete', kwargs={'pk': self.product_user_2.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_exists_delete_product(self):
        product = Product.objects.create(user=self.test_user_1, category=self.category)
        pk = product.pk
        exists = True
        self.client.login(username='TestUser1', password='TestUser1')
        self.client.post(reverse('lk:product_delete', kwargs={'pk': pk}))
        try:
            Product.objects.get(pk=pk)
        except ObjectDoesNotExist:
            exists = False
        self.assertFalse(exists)


class ProductUpdateViewTestCase(TestCase):
    """Test case for profile view"""

    def setUp(self) -> None:
        self.test_user_1 = User.objects.create_user(username='TestUser1', password='TestUser1')
        self.test_user_2 = User.objects.create_user(username='TestUser2', password='TestUser2')

        self.category = Categories.objects.create(id=1, name='TestCategory1', h1='TestCategory1_H1')

        number_product = 30
        for product_number in range(number_product):
            if product_number < 15:
                Product.objects.create(name=f'TestProduct{product_number}', user=self.test_user_1,
                                       category=self.category)
            else:
                Product.objects.create(name=f'TestProduct{product_number}', user=self.test_user_2,
                                       category=self.category)

        self.product = Product.objects.get(name='TestProduct1')
        self.product_user_2 = Product.objects.get(name='TestProduct20')

        # category value in select input dynamically changing with each next request for +1
        self.form_data = {
            'name': 'Test',
            'category': 1,
            'user': str(self.test_user_1),
            'sex': 'Мальчик',
            'breed': 'Метис',
        }

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('lk:product_update', kwargs={'pk': self.product.pk}))
        self.assertRedirects(resp,
                             f'/accounts/login/?next={reverse("lk:product_update", kwargs={"pk": self.product.pk})}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:product_update', kwargs={'pk': self.product.pk}))

        # Checking that the user is logged in
        self.assertEqual(str(resp.context['user']), 'TestUser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lk/product_update.html')

    def test_success_url_form_valid_update_product(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.post(reverse('lk:product_update', kwargs={'pk': self.product.pk}), self.form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('lk:product_list'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.post(reverse('lk:product_update', kwargs={'pk': self.product_user_2.pk}), self.form_data)
        self.assertEqual(resp.status_code, 404)

    def test_update_product(self):
        self.client.login(username='TestUser1', password='TestUser1')

        form_data = self.form_data
        form_data.update({'name': 'ChangeName'})
        resp = self.client.post(reverse('lk:product_update', kwargs={'pk': self.product.pk}), form_data)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'ChangeName')


class ProductCreateViewTestCase(TestCase):
    """Test case for profile view"""

    def setUp(self) -> None:
        self.test_user_1 = User.objects.create_user(username='TestUser1', password='TestUser1')
        self.category = Categories.objects.create(id=1, name='TestCategory1', h1='TestCategory1_H1')

        # category value in select input dynamically changing with each next request for +1
        self.form_data = {
            'name': 'Test',
            'category': 1,
            'sex': 'Мальчик',
            'breed': 'Метис',
        }

    def test_redirect_if_not_logged_in(self):
        resp = self.client.post(reverse('lk:product_create'))
        self.assertRedirects(resp,
                             f'/accounts/login/?next={reverse("lk:product_create")}')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.get(reverse('lk:product_create'))

        # Checking that the user is logged in
        self.assertEqual(str(resp.context['user']), 'TestUser1')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'lk/product_create.html')

    def test_success_url_form_valid_create_product(self):
        self.client.login(username='TestUser1', password='TestUser1')
        resp = self.client.post(reverse('lk:product_create'), self.form_data)
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse('lk:product_list'))

    def test_create_product_with_user_creator(self):
        self.client.login(username='TestUser1', password='TestUser1')
        self.client.post(reverse('lk:product_create'), self.form_data)
        product = Product.objects.get(name='Test')
        self.assertTrue(product)
        self.assertEqual(product.user, self.test_user_1)
