from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Categories, BlogTags, Post
from django.urls import reverse


class PostDetailTestCase(TestCase):
    """Test case for post detail view"""

    def setUp(self) -> None:
        category = Categories.objects.create(name='Category 1')
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        self.post = Post.objects.create(name=f'Post detail', author=user, category=category)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/blog/post/{self.post.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(reverse('blog:post_detail', kwargs={'slug': self.post.slug}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_detail.html')


class CategoriesDetailTestCase(TestCase):
    """Test case for categories detail view"""

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self) -> None:
        self.category = Categories.objects.create(name='Category 1')
        self.category_2 = Categories.objects.create(name='Category 2')
        self.user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        self.path = reverse('blog:categories_detail', kwargs={'slug': self.category.slug})

        number_of_post = 20
        for post_number in range(number_of_post):
            if post_number < 15:
                Post.objects.create(name=f'Post {number_of_post}', author=self.user, category=self.category)
            else:
                Post.objects.create(name=f'Post {number_of_post}', author=self.user, category=self.category_2)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/blog/{self.category.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/categories_detail.html')

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

    def test_post_list_for_category(self):
        resp = self.client.get(f'/blog/{self.category_2.slug}/')
        for post in resp.context['post_list']:
            self.assertEqual(post.category, self.category_2)


class CategoriesListTestCase(TestCase):
    """Test case for categories list view"""

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        categories_number = 15
        for category_number in range(categories_number):
            category = Categories.objects.create(name=f'Category {category_number}')
            Post.objects.create(name=f'Post {category_number}', author=user, category=category)

    def setUp(self) -> None:
        self.path = reverse('blog:categories_list')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/categories/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/blog_main.html')

    def test_view_top_3_categories(self):
        resp = self.client.get(self.path)
        self.assertEqual(len(resp.context['categories_list']), 3)

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


class BlogTagsDetailViewTestCase(TestCase):
    """Test case for blog tags detail view"""

    def setUp(self) -> None:
        self.category = Categories.objects.create(name='Category 1')
        self.tag = BlogTags.objects.create(name='BlogTags 1')
        self.tag_2 = BlogTags.objects.create(name='BlogTags 2')
        self.user = User.objects.create_user(username='Test User', email='test@test.ru', password='Test')
        self.path = reverse('blog:tag_detail', kwargs={'slug': self.tag.slug})

        number_of_post = 20
        for post_number in range(number_of_post):
            if post_number < 15:
                post = Post.objects.create(name=f'Post {number_of_post}', author=self.user, category=self.category)
                post.tags.set([self.tag])
            else:
                post = Post.objects.create(name=f'Post {number_of_post}', author=self.user, category=self.category)
                post.tags.set([self.tag_2])

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/blog/tag/{self.tag.slug}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_accessible_by_name_and_uses_correct_template(self):
        resp = self.client.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/tag_detail.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(self.path)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['post_list']) == 10)

    def test_lists_all_product(self):
        resp = self.client.get(self.path + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['post_list']) == 5)

    def test_product_list_for_tag(self):
        resp = self.client.get(f'/blog/tag/{self.tag_2.slug}/')
        for post in resp.context['post_list']:
            self.assertIn(self.tag_2, post.tags.all())
