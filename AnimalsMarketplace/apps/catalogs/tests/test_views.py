from django.contrib.auth.models import User
from django.test import TestCase

from catalogs.models import Product, Categories
from django.urls import reverse


class ProductListTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Category 1', h1='Category 1', )
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        # create 15 product for pagination test
        number_of_product = 15
        for product_number in range(number_of_product):
            Product.objects.create(name=f'Product {product_number}', user=user, category=category)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/product/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(reverse('catalogs:product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalogs/product_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('catalogs:product_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['product_list']) == 10)
