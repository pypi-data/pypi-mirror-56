import sys
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile


class CompressImageFieldFile(ImageFieldFile):
	def save(self, name, content, save=True):
		"""
		Updating content before saving
		"""
		content = self.compress_image(content)
		super().save(name, content, save)

	def compress_image(self, file):
		"""
		Update MemoryUploadFile Object for compress image
		and changes Dimension if we pass dim
		"""
		temp_image = Image.open(file)
		output_io = BytesIO()
		if self.field.dim:
			temp_image = temp_image.resize(self.field.dim)
		temp_image.save(output_io, format=file.image.format, optimize=True)
		output_io.seek(0)
		return InMemoryUploadedFile(output_io, 'ImageField', f"{file.name}",
									f'{file.content_type}', sys.getsizeof(output_io), None)


class CompressImageField(ImageField):
	attr_class = CompressImageFieldFile

	def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, dim=None, **kwargs):
		self.width_field, self.height_field, self.dim = width_field, height_field, dim
		super().__init__(verbose_name, name, **kwargs)
