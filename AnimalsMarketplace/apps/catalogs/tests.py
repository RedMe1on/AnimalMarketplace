from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.test import TestCase

# Create your tests here.
from pytils.translit import slugify

from catalogs.models import Categories, Product


# Test models
class CategoriesModelTestCase(TestCase):
    """Test model Categories"""

    @classmethod
    def setUpTestData(cls):
        Categories.objects.create(name='Category 1', h1='Category 1', )

    def test_get_absolute_url(self):
        category = Categories.objects.get(id=1)
        self.assertEqual(category.get_absolute_url(), f'/{category.slug}/')

    def test_save_without_slug(self):
        category_without_slug = Categories(name='Category 2', h1='Category 2')
        category_without_slug.save()
        self.assertEqual(category_without_slug.slug, slugify(category_without_slug.h1))

    def test_save_with_slug(self):
        category_with_slug = Categories(name='Category 2', h1='Category 2',
                                        slug='teSt slug with space-and_other символы')
        start_slug = category_with_slug.slug
        category_with_slug.save()
        self.assertEqual(category_with_slug.slug, slugify(start_slug))

    def test_save_with_none_unique_slug(self):
        category_1 = Categories(name='Category 2', h1='Category 2', slug='Unique')
        category_2 = Categories(name='Category 2', h1='Category 2', slug='Unique')
        start_slug_category_2 = category_2.slug
        category_1.save()
        category_2.save()
        self.assertEqual(category_2.slug, slugify(start_slug_category_2) + '-copy')

    def test_str_method(self):
        category = Categories.objects.get(id=1)
        expected_object_name = category.name
        self.assertEqual(str(category), expected_object_name)


class ProductModelTestCase(TestCase):
    """Test model Product"""

    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Category 1', h1='Category 1', )
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        Product.objects.create(name='Product 1', user=user, category=category)

    def setUp(self) -> None:
        self.product = Product.objects.get(id=1)

    def test_get_absolute_url(self):
        self.assertEqual(self.product.get_absolute_url(), f'/product/{self.product.pk}/')

    def test_get_update_url(self):
        self.assertEqual(self.product.get_update_url(), f'/lk/product/{self.product.pk}/update/')

    def test_get_delete_url(self):
        self.assertEqual(self.product.get_delete_url(), f'/lk/product/{self.product.pk}/delete/')

# Test forms

class FilterFormTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
# class CategoriesDetailTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#
#
#
#     def setUp(self) -> None:
#         parent = Categories.objects.create(name='Родитель', h1='Родитель')
#         child_1 = Categories.objects.create(name='Ребенок Родителя', h1='Ребенок Родителя', parent=parent)
#         child_child_1 = Categories.objects.create(name='Ребенок Ребенка Родителя', h1='Ребенок Ребенка Родителя',
#                                                   parent=child_1)
#
#     def test_get_child_and_self_categories(self):
#         parent = Categories.objects.get(name='Родитель')
#         child_1 = Categories.objects.get(name='Ребенок Родителя')
#         child_child_1 = Categories.objects.get(name='Ребенок Ребенка Родителя')
#
#         self.assertEqual(parent.get_child_and_self_categories(parent.slug), QuerySet([parent]))
#         self.assertEqual(parent.get_child_and_self_categories(child_1.slug), QuerySet([parent, child_1]))
#         self.assertEqual(parent.get_child_and_self_categories(child_child_1.slug), QuerySet([parent, child_1, child_child_1]))
