from django.db.models import QuerySet
from django.test import TestCase

# Create your tests here.
from .models import Categories


class CategoriesDetailTestCase(TestCase):
    def setUp(self) -> None:
        parent = Categories.objects.create(name='Родитель', h1='Родитель')
        child_1 = Categories.objects.create(name='Ребенок Родителя', h1='Ребенок Родителя', parent=parent)
        child_child_1 = Categories.objects.create(name='Ребенок Ребенка Родителя', h1='Ребенок Ребенка Родителя',
                                                  parent=child_1)

    def test_get_child_and_self_categories(self):
        parent = Categories.objects.get(name='Родитель')
        child_1 = Categories.objects.get(name='Ребенок Родителя')
        child_child_1 = Categories.objects.get(name='Ребенок Ребенка Родителя')

        self.assertEqual(parent.get_child_and_self_categories(parent.slug), QuerySet([parent]))
        self.assertEqual(parent.get_child_and_self_categories(child_1.slug), QuerySet([parent, child_1]))
        self.assertEqual(parent.get_child_and_self_categories(child_child_1.slug), QuerySet([parent, child_1, child_child_1]))