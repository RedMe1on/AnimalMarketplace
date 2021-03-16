from django.contrib.auth.models import User
from django.test import TestCase
from pytils.translit import slugify
from catalogs.models import Categories, Product, BreedType



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
        category_3 = Categories(name='Category 2', h1='Category 2', slug='Unique')
        category_4 = Categories(name='Category 2', h1='Category 2', slug='Unique')
        start_slug_category_2 = category_2.slug
        start_slug_category_3 = category_3.slug
        start_slug_category_4 = category_4.slug
        category_1.save()
        category_2.save()
        category_3.save()
        category_4.save()
        self.assertEqual(category_2.slug, slugify(start_slug_category_2) + '-copy')
        self.assertEqual(category_3.slug, slugify(start_slug_category_3) + '-copy-copy')
        self.assertEqual(category_4.slug, slugify(start_slug_category_4) + '-copy-copy-copy')

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

    def test_str_method(self):
        expected_object_name = self.product.name
        self.assertEqual(str(self.product), expected_object_name)


class BreedTypeModelTestCase(TestCase):
    """Test model BreedType"""

    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name='Category 1', h1='Category 1', )
        BreedType.objects.create(id=1, name='BreedType 1', category=category)

    def setUp(self) -> None:
        self.breed_type = BreedType.objects.get(id=1)

    def test_str_method(self):
        expected_object_name = self.breed_type.name
        self.assertEqual(str(self.breed_type), expected_object_name)