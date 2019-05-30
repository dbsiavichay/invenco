# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from django.forms import modelformset_factory, formset_factory

from .models import *
from .forms import ReplyForm, ReplacementForm

from stocktaking.models import Type

from pure_pagination.mixins import PaginationMixin


class TicketListView(PaginationMixin, ListView):
	model = Ticket
	paginate_by = 20

class TicketUserListView(TicketListView):
	def get_queryset(self):
		queryset = super(TicketUserListView, self).get_queryset()
		queryset = queryset.filter(user=self.request.user)
		return queryset

class TicketCreateView(CreateView):
	model = Ticket
	fields = ('problem_type', 'equipment', 'problem')
	success_url = reverse_lazy('ticket_list')

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return redirect(self.success_url)

class TicketUpdateView(UpdateView):
	model = Ticket
	fields = ('problem_type', 'equipment', 'problem')
	success_url = reverse_lazy('ticket_list')

class TicketDetailView(DetailView):
	model = Ticket

class ReplyBaseCreateView(CreateView):
	model = Reply
	form_class = ReplyForm
	success_url = reverse_lazy('ticket_list')


	def form_valid(self, form):
		self.object = form.save()
		self.update_ticket(self.object.ticket)		
		return redirect(self.success_url)
		
	def get_ticket(self):
		pk = self.kwargs.get('pk') or self.request.GET.get('pk') or None
		ticket = get_object_or_404(Ticket, pk=pk)		
		return ticket

	def update_ticket(self, ticket):
		pass

	def get_initial(self):
		initial = super(ReplyBaseCreateView, self).get_initial()
		initial.update({
			'ticket': self.get_ticket()
		})
		return initial

	def get(self, request, *args, **kwargs):
		ticket = self.get_ticket()
		if ticket.status > ticket.OPEN or ticket.user != request.user:
			return redirect(reverse_lazy('ticket_detail', args=[ticket.id]))
		return super(ReplyBaseCreateView, self).get(request, *args, **kwargs)

class ReplySolvedCreateView(ReplyBaseCreateView):
	template_name='maintenance/reply_solved_form.html'

	def get_context_data(self, **kwargs):
		context = super(ReplySolvedCreateView, self).get_context_data(**kwargs)
		types = Type.objects.filter(usage=Type.REPLACEMENT)
		formset = self.get_replacement_formset()		
		context.update({'types': types,})
		return context

	def form_valid(self, form):
		formset = self.get_replacement_formset()		
		if not formset.is_valid():
			return self.form_invalid(form)

		self.object = form.save()

		for form in formset:
			replacement = form.cleaned_data['replacement']
			replacement.code = form.cleaned_data['serial']
			replacement.serial = form.cleaned_data['serial']
			replacement.reply = self.object
			replacement.save()
			

		self.update_ticket(self.object.ticket)
		return redirect(self.success_url)

	def update_ticket(self, ticket):
		ticket.status = Ticket.SOLVED
		ticket.save()

	def get_replacement_formset(self):
		ReplacementFormset = formset_factory(ReplacementForm, extra=0)
		formset = ReplacementFormset(self.request.POST)
		return formset

class ReplyClosedCreateView(ReplyBaseCreateView):
	template_name='maintenance/reply_closed_form.html'

	def update_ticket(self, ticket):
		ticket.status = Ticket.CLOSED
		ticket.save()

class ReplyCanceledCreateView(ReplyBaseCreateView):
	template_name='maintenance/reply_canceled_form.html'

	def update_ticket(self, ticket):
		ticket.status = Ticket.CANCELED
		ticket.save()

def get_component(request, pk):
	from django.template.loader import render_to_string	
	type = get_object_or_404(Type, pk=pk)
	form = ReplacementForm(type=type)
	r = render_to_string('components/maintenance/replacement_form.html', context={'form':form})
	return JsonResponse({'form': r}, status=200)