from django.contrib.auth.models import User
from django.test import TestCase
from moderation.helpers import automoderate
from rest_framework.test import APIClient
from catalogs.models import Product, Categories, BreedType, ReportModel
from django.urls import reverse
from django.test import override_settings


class ProductListTestCase(TestCase):
    """Test Case for Product list view"""

    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Category 1')
        my_admin = User.objects.create_superuser(username='myuser', email='myemail@test.com', password='password')
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        breed_type_1 = BreedType.objects.create(id=1, name='Породистый 1', category=category)
        breed_type_2 = BreedType.objects.create(id=2, name='Породистый 2', category=category)
        # create 15 product for pagination test
        number_of_product = 15
        for product_number in range(number_of_product):
            if product_number >= 10:
                breed = 'Метис'
                sex = 'Девочка'
                breed_type = breed_type_1
            else:
                breed = 'Породистый'
                sex = 'Мальчик'
                breed_type = breed_type_2
            product = Product.objects.create(name=f'Product {product_number}', user=user, category=category, sex=sex,
                                             price=f'{product_number}', breed=breed, breed_type=breed_type,
                                             is_visible=True)
            automoderate(product, my_admin)

    def setUp(self) -> None:
        self.breed_type = BreedType.objects.get(id=1)
        self.breed_type_2 = BreedType.objects.get(id=2)

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
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['product_list']) == 10)

    def test_lists_all_product(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
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
        resp = self.client.get(reverse('catalogs:product_list') + '?breed_type=1')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.breed_type == self.breed_type)

    def test_filter_product_breed_type_field_multiply(self):
        resp = self.client.get(reverse('catalogs:product_list') + '?breed_type=1&breed_type=2')
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(product.breed_type == self.breed_type or product.breed_type == self.breed_type_2)

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
        string = '?sex=Мальчик&price_start=10&price_end=14&breed=Породистый&breed=Метис&breed_type=1&breed_type=2'
        resp = self.client.get(reverse('catalogs:product_list') + string)
        self.assertEqual(resp.status_code, 200)
        for product in resp.context['product_list']:
            self.assertTrue(10 <= product.price < 15)
            self.assertTrue(product.sex == 'Мальчик')
            self.assertTrue(product.breed == 'Породистый' or product.breed == 'Метис')
            self.assertTrue(product.breed_type == self.breed_type or product.breed_type == self.breed_type_2)


class CategoriesListTestCase(TestCase):
    """Test case for categories list view"""

    @classmethod
    def setUpTestData(cls):
        categories_number = 5
        for category in range(categories_number):
            Categories.objects.create(name=f'Category {category}')

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
        category = Categories.objects.create(name='Category 1')
        my_admin = User.objects.create_superuser(username='myuser', email='myemail@test.com', password='password')
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        # create 15 product for pagination test
        number_of_product = 15
        for product_number in range(number_of_product):
            product = Product.objects.create(name=f'Product {product_number}', user=user, category=category)
            automoderate(product, my_admin)

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
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['product_list']) == 10)

    def test_lists_all_product(self):
        resp = self.client.get(f'/{self.category.slug}/' + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['product_list']) == 5)

    def test_product_list_for_category(self):

        parent_category = Categories.objects.create(name=f'Parent')
        Product.objects.create(name=f'Product parent', user=self.user, category=parent_category)

        amount_of_children = 3
        for child_number in range(amount_of_children):
            category = Categories.objects.create(name=f'Child {child_number}', parent=parent_category)
            Product.objects.create(name=f'Product {child_number}', user=self.user, category=category)

        resp = self.client.get(f'/{parent_category.slug}/')
        self.assertEqual(resp.status_code, 200)

        for product in resp.context['product_list']:
            self.assertIn(product.category, parent_category.get_descendants(include_self=True))


class ProductDetailTestCase(TestCase):
    """Test case for product detail view"""

    def setUp(self) -> None:
        my_admin = User.objects.create_superuser(username='myuser', email='myemail@test.com', password='password')
        category = Categories.objects.create(name='Category 1')
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        self.product = Product.objects.create(name=f'Product detail', user=user, category=category)
        automoderate(self.product, my_admin)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/product/{self.product.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(f'/product/{self.product.pk}/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalogs/product_detail.html')


class BreedTypeListAPIViewTestCase(TestCase):
    """Test case for BreedTypeAPI view"""

    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(id=1, name='Category 1')
        category_2 = Categories.objects.create(id=2, name='Category 2')
        number_breed_type = 5
        for number in range(number_breed_type):
            if number < 3:
                BreedType.objects.create(name=f'BreedType {number}', category=category)
            else:
                BreedType.objects.create(name=f'BreedType {number}', category=category_2)

    def setUp(self) -> None:
        self.client_api = APIClient()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/api/v1/breedtype/')
        self.assertEqual(resp.status_code, 200)

    def test_get_data(self):
        resp = self.client_api.get('http://127.0.0.1:8000/api/v1/breedtype/')
        self.assertEqual(resp.status_code, 200)
        for json_dict in resp.json():
            self.assertTrue(BreedType.objects.get(id=json_dict.get('id'), name=json_dict.get('name'),
                                                  category=json_dict.get('category')))

    def test_get_data_with_filter_by_category(self):
        resp = self.client_api.get('http://127.0.0.1:8000/api/v1/breedtype/?category=1')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(len(resp.json()) == 3)

        for json_dict in resp.json():
            self.assertTrue(BreedType.objects.get(id=json_dict.get('id'), name=json_dict.get('name'),
                                                  category=json_dict.get('category')))
            self.assertTrue(json_dict['category'] == 1)


class SuccessReportViewTestCase(TestCase):
    """Test case for view SuccessReport"""

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/report/success/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_accessible_by_name(self):
        resp = self.client.get(reverse('catalogs:report_success'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalogs/report_success.html')


class ReportViewTestCase(TestCase):
    """Test case for view Report"""

    def setUp(self) -> None:
        category = Categories.objects.create(name='Category 1')
        my_admin = User.objects.create_superuser(username='myuser', email='myemail@test.com', password='password')
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        self.product = Product.objects.create(id=1, name=f'Product Test', user=user, category=category)
        automoderate(self.product, my_admin)
        self.form_data = {
            'cause': 'Указан чужой номер телефона',
        }

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/report/{self.product.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template_and_accessible_by_name(self):
        resp = self.client.get(reverse('catalogs:report', kwargs={'pk': self.product.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'catalogs/report.html')

    def test_success_url_form_valid_renewal_profile(self):
        form_data = self.form_data
        form_data['comment'] = 'Test comment'
        resp = self.client.post(reverse('catalogs:report', kwargs={'pk': self.product.pk}), form_data)
        self.assertRedirects(resp, reverse('catalogs:report_success'))

    def test_optional_field_comment(self):
        resp = self.client.post(reverse('catalogs:report', kwargs={'pk': self.product.pk}), self.form_data)
        self.assertRedirects(resp, reverse('catalogs:report_success'))

    def test_write_in_product_field_in_form(self):
        self.client.post(reverse('catalogs:report', kwargs={'pk': self.product.pk}), self.form_data)
        reports = ReportModel.objects.all()
        for report in reports:
            self.assertEqual(report.product, self.product)
