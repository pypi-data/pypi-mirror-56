import os

from django.conf import settings
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse


class CompressImageTest(TestCase):
	def setUp(self):
		self.c = Client()
		self.path = os.path.join(settings.BASE_DIR, 'user.jpg')
		image = open(self.path, 'rb')
		url = reverse('compress-image')
		self.object = self.c.post(url, {'image': image})

	def test_image_size(self):
		data = self.object.json()
		size = os.stat(self.path).st_size
		self.assertLessEqual(data['size'], size)


class DimensionImageTest(TestCase):
	def setUp(self):
		self.c = Client()
		self.path = os.path.join(settings.BASE_DIR, 'user.jpg')
		image = open(self.path, 'rb')
		url = reverse('dimension-image')
		self.object = self.c.post(url, {'image': image})

	def test_image_width(self):
		dim = self.object.json()['dim']
		self.assertEqual(100, dim[0])

	def test_image_height(self):
		dim = self.object.json()['dim']
		self.assertEqual(100, dim[1])
