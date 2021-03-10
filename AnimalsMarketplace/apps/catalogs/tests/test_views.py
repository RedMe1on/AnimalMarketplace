from django.contrib.auth.models import User
from django.test import TestCase

from catalogs.models import Product, Categories
from django.urls import reverse


class ProductListTestCase(TestCase):
    """Test Case for Product list view"""

    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Category 1', h1='Category 1', )
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        # create 15 product for pagination test
        number_of_product = 15
        for product_number in range(number_of_product):
            if product_number >= 10:
                breed = 'Метис'
                sex = 'Девочка'
                breed_type = ''
            else:
                breed = 'Породистый'
                sex = 'Мальчик'
                breed_type = 'Породистый'
            Product.objects.create(name=f'Product {product_number}', user=user, category=category, sex=sex,
                                   price=f'{product_number}', breed=breed, breed_type=breed_type)

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

    def test_lists_all_product(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['product_list']) == 5)

    def test_filter_product_sex_field(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?sex=Мальчик')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.sex == 'Мальчик')

    def test_filter_product_breed_field(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?breed=Породистый')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.breed == 'Породистый')

    def test_filter_product_breed_field_multiply(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?breed=Породистый&breed=Метис')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.breed == 'Породистый' or product.breed == 'Метис')

    def test_filter_product_breed_type_field(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?breed_type=Породистый')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.breed == 'Породистый')

    def test_filter_product_breed_type_field_multiply(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?breed_type=Породистый&breed_type=')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.breed_type == 'Породистый' or product.breed_type == '')

    def test_filter_product_image_type_field(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?image=on')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.context['product_list']) == 0)

    def test_filter_product_price_start_field(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?price_start=10')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.price >= 10)

    def test_filter_product_price_end_field(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?price_end=15')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.price < 15)

    def test_filter_product_all_fields_at_the_same_time(self):
        string = '?sex=Мальчик&price_start=10&price_end=14&breed=Породистый&breed=Метис&breed_type=Породистый'
        resp = self.client.get(reverse('catalogs:product_list') + string)
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(10 <= product.price < 15)
            self.assertTrue(product.sex == 'Мальчик')
            self.assertTrue(product.breed == 'Породистый' or product.breed == 'Метис')
            self.assertTrue(product.breed_type == 'Породистый' or product.breed_type == '')


class CategoriesListTestCase(TestCase):
    """Test case for categories list view"""

    @classmethod
    def setUpTestData(cls):
        categories_number = 5
        for category in range(categories_number):
            Categories.objects.create(name=f'Category {category}', h1=f'Category {category}', )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/categories/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(reverse('catalogs:categories_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalogs/categories_list.html')


class CategoriesDetailTestCase(TestCase):
    """Test case for categories detail view"""

    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Category 1', h1='Category 1', )
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        # create 15 product for pagination test
        number_of_product = 15
        for product_number in range(number_of_product):
            Product.objects.create(name=f'Product {product_number}', user=user, category=category)

    def setUp(self) -> None:
        self.category = Categories.objects.get(name='Category 1')
        self.user = User.objects.get(username='Test User')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/{self.category.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(f'/{self.category.slug}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalogs/categories_detail.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(f'/{self.category.slug}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['product_list']) == 10)

    def test_lists_all_product(self):
        resp = self.client.get(f'/{self.category.slug}/' + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['product_list']) == 5)

    def test_product_list_for_category(self):

        parent_category = Categories.objects.create(name=f'Parent', h1=f'Parent')
        Product.objects.create(name=f'Product parent', user=self.user, category=parent_category)

        amount_of_children = 3
        for child in range(amount_of_children):
            category = Categories.objects.create(name=f'Child {child}', h1=f'Child {child}', parent=parent_category)
            Product.objects.create(name=f'Product {child}', user=self.user, category=category)

        resp = self.client.get(f'/{parent_category.slug}/')
        self.assertEqual(resp.status_code, 200)

        for product in resp.context['product_list']:
            self.assertIn(product.category, parent_category.get_descendants(include_self=True))


class ProductDetailTestCase(TestCase):
    """Test case for product detail view"""

    def setUp(self) -> None:
        category = Categories.objects.create(name='Category 1', h1='Category 1', )
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        self.product = Product.objects.create(name=f'Product detail', user=user, category=category)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/product/{self.product.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(f'/product/{self.product.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalogs/product_detail.html')


