from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import CreateView

from testapp.models import TestCompressImageModel, TestDimensionImageModel


class CompressImageView(CreateView):
	model = TestCompressImageModel
	fields = ('image',)
	template_name = 'image.html'

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		obj = form.save()
		data = {'size': obj.image.size}
		return JsonResponse(data, status=201)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse('compress-image')
		return context


class DimensionImageView(CreateView):
	model = TestDimensionImageModel
	fields = ('image',)
	template_name = 'image.html'

	def form_valid(self, form):
		"""If the form is valid, save the associated model."""
		obj = form.save()
		data = {'dim': obj.image._get_image_dimensions()}
		return JsonResponse(data, status=201)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['url'] = reverse('dimension-image')
		return context
