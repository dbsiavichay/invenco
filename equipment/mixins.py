from django.db.models import Q
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse, Http404

class ListViewMixin(object):
    def get_filter_objects(self, fields):
        keyword = self.request.GET.get('keyword', None)
        if keyword is not None:
            args_list = []
            filter_args = Q()
            for field in fields:
                args_list.append(Q(**{field+'__icontains': str(keyword)}))

            for q in args_list:
                filter_args = filter_args | q

            num_page = self.request.GET.get('page', None)
            queryset = self.model.objects.filter(*(filter_args,))
            paginator = self.get_paginator(queryset, self.paginate_by)
            page = paginator.page(num_page) if num_page is not None else paginator.page(1)
            data = {
				'object_list': page.object_list,
				'has_next': page.has_next(),
				'next_page_number': page.next_page_number() if page.has_next() else -1
			}
            return data
        else:
            return {}

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            fields = [field.name for field in self.model._meta.fields if field.name != 'id']
            print fields
            modelform = modelform_factory(self.model, fields=fields)
            form = modelform(request.POST)
            if form.is_valid():
                obj = form.save()
                data = model_to_dict(obj)
                return JsonResponse(data)
            return JsonResponse({}, status=400)

class DetailViewMixin(object):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            fields = [field.name for field in self.model._meta.fields if field.name != 'id']
            modelform = modelform_factory(self.model, fields=fields)
            form = modelform(self.request.POST, instance=self.object)
            if form.is_valid():
                form.save()
                data = model_to_dict(self.object)
                return JsonResponse(data)
            return JsonResponse({}, status=400)

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})
