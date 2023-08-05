from django.db import models

from djimage.field import CompressImageField


class TestCompressImageModel(models.Model):
	image = CompressImageField(upload_to='compress/')


class TestDimensionImageModel(models.Model):
	image = CompressImageField(upload_to='dimension/', dim=(100, 100))
