from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from equipment.models import Device
from organization.models import Contributor

class HomeView(ListView):
    model = Device
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        charter = self.request.GET.get('charter', None)
        context['message'] = ''
        context['object_list'] = []
        if charter is not None:
            lst = Contributor.objects.using('sim').filter(charter=charter)
            cont = lst[0] if len(lst) > 0 else None
            if cont is not None:
                context['message'] = cont.name
                context['object_list'] = self.model.objects.filter(allocation__is_active=True, allocation__employee=cont.charter)
            else:
                context['message'] = 'Cedula incorrecta'

        return context
