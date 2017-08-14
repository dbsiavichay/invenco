from django import forms
from django.forms import formset_factory, ModelForm
from stocktaking.models import Replacement

from functools import partial, wraps

class ReplacementForm(ModelForm):
	class Meta:
		model = Replacement
		fields = ('quantity', 'unit_price', 'stock', 'movement', 'model')
		widgets = {
            'model': forms.HiddenInput,
            'unit_price': forms.HiddenInput,
            'stock': forms.HiddenInput,
            'movement': forms.HiddenInput,
        }
        	

	def __init__(self, *args, **kwargs):
		replacements = kwargs.pop('replacements', None)
		replacement = replacements.pop(0)		

		initial = kwargs.get('initial', {})

		initial.update({
			'quantity': 0,
			'unit_price': replacement.unit_price,
			'stock': replacement.stock,
			'movement': Replacement.OUT_BY_FIX,
			'model': replacement.model.id
		})

		kwargs['initial'] = initial

		super(ReplacementForm, self).__init__(*args, **kwargs)

		self.fields['quantity'].widget.attrs.update({'min': 0, 'max': replacement.stock})		
		self.fields['stock'].required = False
		self.fields['model'].label = '%s %s' % (replacement.model.type, replacement.model)
		

def get_replacement_formset():
	replacements = Replacement.objects.order_by('model__name', '-date_joined').distinct('model__name').filter(stock__gt=0)
	
	return formset_factory(			
		wraps(ReplacementForm)(partial(ReplacementForm, replacements=list(replacements))),		
		extra=len(replacements)
	)
