import operator
from django.views.generic import ListView
from django.db.models import Q
from .models import Type, Model

class SearchMixin(object):
	def get_queryset(self):			
		queryset = super(SearchMixin, self).get_queryset()
		queryset = self.search_by_type(queryset)
		queryset = self.search_by_keyword(queryset, self.search_fields)
		return queryset

	def search_by_type(self, queryset):
		type = self.get_type()
		if type is not None:			
			field = 'type' if self.model == Model else 'model__type'
			queryset = queryset.filter(**{field:type})
		return queryset 

	def search_by_keyword(self, queryset, fields=['id',]):
		keyword = self.request.GET.get('search') or self.kwargs.get('search') or None
		if keyword is not None:			
			args = [Q(**{field+'__icontains': keyword}) for field in fields]
			queryset = queryset.filter(reduce(operator.__or__, args))				

		return queryset

	def get_type(self):
		pk = self.request.GET.get('type') or self.kwargs.get('type') or None		
		try:					
			type = Type.objects.get(pk=pk)			
			return type
		except:
			return None


# if search is not None:
# 			fields = ['model__name', 'model__brand__name', 'model__part_number', 'code', 'serial', 'specifications']
		
# 			args = [Q(**{field+'__icontains': search}) for field in fields]

# 			charters = Employee.objects.using('sim').filter(
# 				Q(contributor__charter=search) | Q(contributor__name__icontains=search)
# 			).values_list('contributor__charter', flat=True)

# 			if len(charters) > 0: args.append(Q(owner__in=list(charters)))

# 			queryset = queryset.filter(reduce(operator.__or__, args))