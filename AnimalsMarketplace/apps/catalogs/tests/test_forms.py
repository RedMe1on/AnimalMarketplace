from django.test import SimpleTestCase
from catalogs.forms import FilterForm


class FilterFormTestCase(SimpleTestCase):
    """Test case for Filter form"""

    def test_optional_fields(self):
        form_data = {}
        form = FilterForm(form_data)
        self.assertTrue(form.is_valid())

    def test_price_start_min_value(self):
        form_data = {
            'price_start': -1
        }
        form = FilterForm(form_data)
        self.assertFalse(form.is_valid())

    def test_price_end_min_value(self):
        form_data = {
            'price_end': -1
        }
        form = FilterForm(form_data)
        self.assertFalse(form.is_valid())
