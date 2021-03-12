from django.test import TestCase

from blog.models import Categories, BlogTags, Post
from pytils.translit import slugify


class CategoriesModelTestCase(TestCase):
    """Test case for model Categories"""

    def setUp(self):
        self.category = Categories.objects.create(name='Category 1')

    def test_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(), f'/blog/{self.category.slug}/')

    def test_save_without_slug(self):
        category_without_slug = Categories(name='Category 2')
        category_without_slug.save()
        self.assertEqual(category_without_slug.slug, slugify(category_without_slug.name))

    def test_save_with_slug(self):
        category_with_slug = Categories(name='Category 2', slug='teSt slug with space-and_other символы')
        start_slug = category_with_slug.slug
        category_with_slug.save()
        self.assertEqual(category_with_slug.slug, slugify(start_slug))

    def test_save_with_none_unique_slug(self):
        category_1 = Categories(name='Category 2', slug='Unique')
        category_2 = Categories(name='Category 2', slug='Unique')
        start_slug_category_2 = category_2.slug
        category_1.save()
        category_2.save()
        self.assertEqual(category_2.slug, slugify(start_slug_category_2) + '-copy')

    def test_str_method(self):
        expected_object_name = self.category.name
        self.assertEqual(str(self.category), expected_object_name)


class BlogTagsModelTestCase(TestCase):
    """Test case for model BlogTags"""

    def setUp(self):
        self.tag = BlogTags.objects.create(name='Test Tag 1')

    def test_get_absolute_url(self):
        self.assertEqual(self.tag.get_absolute_url(), f'/blog/tag/{self.tag.slug}/')

    def test_save_without_slug(self):
        tag_without_slug = BlogTags(name='Test Tag 2')
        tag_without_slug.save()
        self.assertEqual(tag_without_slug.slug, slugify(tag_without_slug.name))

    def test_save_with_slug(self):
        tag_with_slug = BlogTags(name='Test Tag 3', slug='teSt slug with space-and_other символы')
        start_slug = tag_with_slug.slug
        tag_with_slug.save()
        self.assertEqual(tag_with_slug.slug, slugify(start_slug))

    def test_save_with_none_unique_slug(self):
        tag_1 = BlogTags(name='Test Tag 4', slug='Unique')
        tag_2 = BlogTags(name='Test Tag 5', slug='Unique')
        start_slug_tag_2 = tag_2.slug
        tag_1.save()
        tag_2.save()
        self.assertEqual(tag_2.slug, slugify(start_slug_tag_2) + '-copy')

    def test_str_method(self):
        expected_object_name = self.tag.name
        self.assertEqual(str(self.tag), expected_object_name)


class PostModelTestCase(TestCase):
    """Test case for model Post"""

    def setUp(self):
        self.post = Post.objects.create(name='Test Post 1')

    def test_get_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), f'/blog/post/{self.post.slug}/')

    def test_save_without_slug(self):
        post_without_slug = Post(name='Test Tag 2')
        post_without_slug.save()
        self.assertEqual(post_without_slug.slug, slugify(post_without_slug.name))

    def test_save_with_slug(self):
        post_with_slug = Post(name='Test Post 3', slug='teSt slug with space-and_other символы')
        start_slug = post_with_slug.slug
        post_with_slug.save()
        self.assertEqual(post_with_slug.slug, slugify(start_slug))

    def test_save_with_none_unique_slug(self):
        post_1 = Post(name='Test Post 4', slug='Unique')
        post_2 = Post(name='Test Post 5', slug='Unique')
        post_3 = Post(name='Test Post 5', slug='Unique')
        post_4 = Post(name='Test Post 5', slug='Unique')
        start_slug_post_2 = post_2.slug
        start_slug_post_3 = post_3.slug
        start_slug_post_4 = post_4.slug
        post_1.save()
        post_2.save()
        post_3.save()
        post_4.save()
        self.assertEqual(post_2.slug, slugify(start_slug_post_2) + '-copy')
        self.assertEqual(post_3.slug, slugify(start_slug_post_3) + '-copy-copy')
        self.assertEqual(post_4.slug, slugify(start_slug_post_4) + '-copy-copy-copy')

    def test_str_method(self):
        expected_object_name = self.post.name
        self.assertEqual(str(self.post), expected_object_name)
