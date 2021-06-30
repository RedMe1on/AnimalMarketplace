from moderation.helpers import automoderate
from catalogs.models import Product, Categories, BreedType, ReportModel
from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Categories as Categories_blog, BlogTags, Post
from django.urls import reverse


class ProductSearchListTestCase(TestCase):
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
        resp = self.client.get('/search/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(reverse('search:search'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'search/search.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('search:search') + '?q=Product')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_lists_all_product(self):
        resp = self.client.get(reverse('search:search') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['object_list']) == 5)


class PostSearchListTestCase(TestCase):
    """Test case for categories detail view"""

    def setUp(self) -> None:
        self.category = Categories_blog.objects.create(name='Category 1')
        self.category_2 = Categories_blog.objects.create(name='Category 2')
        self.user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        self.path = reverse('search:search')

        number_of_post = 20
        for post_number in range(number_of_post):
            if post_number < 15:
                Post.objects.create(name=f'Post {number_of_post}', author=self.user, category=self.category)
            else:
                Post.objects.create(name=f'Post {number_of_post}', author=self.user, category=self.category_2)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/search/')
        self.assertEqual(resp.status_code, 200)

    def test_view_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'search/search.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['post_list']) == 10)

    def test_lists_all_posts(self):
        resp = self.client.get(self.path + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['post_list']) == 5)

