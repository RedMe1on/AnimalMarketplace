from os import path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from lk.forms import AdditionalImagesProductForm


class TestCaseAdditionalImagesProductForm(SimpleTestCase):
    """Test Case for AdditionalImagesProduct Form"""

    def setUp(self) -> None:
        self.parent_dir = path.dirname(path.abspath(__file__))

    def test_upload_image(self):
        with open(path.join(self.parent_dir, 'image', '1.jpg'), 'rb') as one:
            with open(path.join(self.parent_dir, 'image', '1.jpg'), 'rb') as two:
                file_dict = {'image': [SimpleUploadedFile(one.name, one.read(), 'image/*'), SimpleUploadedFile(two.name, two.read(), 'image/*')]}
                form = AdditionalImagesProductForm(file_dict)
        self.assertTrue(form.is_valid())

