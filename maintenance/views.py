# -*- coding: utf-8 -*-
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

#from django.forms import modelformset_factory, formset_factory

from .models import *
from .forms import ReplyForm

from stocktaking.models import Replacement

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

	def update_ticket(self, ticket):
		ticket.status = Ticket.SOLVED
		ticket.save()

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


class FixListView(PaginationMixin, ListView):
	model = Fix
	paginate_by = 8

	def get_queryset(self):		
		queryset = super(FixListView, self).get_queryset()	
		queryset = queryset.filter(user=self.request.user)
		return queryset

class FixCreateView(CreateView):
	model = Fix
	fields = ('problem', 'solution', 'observation', 'equipment')
	success_url = '/fix/'

	def get_context_data(self, **kwargs):
		context = super(FixCreateView, self).get_context_data(**kwargs)

		#formset = self.get_formset()

		#context.update({			
		#	'formset': formset,
		#})

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()

		#formset = self.get_formset()

		#if not formset.is_valid():
		#	return self.form_invalid(form)

		# for frm in formset:
		# 	last = Replacement.objects.filter(model=frm.cleaned_data['model']).order_by('-date_joined')[0]				

		# 	if frm.cleaned_data.get('quantity') > 0:					
		# 		rep = frm.save(commit=False)				
		# 		rep.total_price = rep.quantity * rep.unit_price
		# 		rep.stock = last.stock - rep.quantity				

		# 		obs = {
		# 			'fix_id':  self.object.id,
		# 			'description': 'Salida por uso en arreglo.'
		# 		}

		# 		rep.observation = str(obs)
		# 		rep.save()

		return redirect(self.get_success_url())

	def get_formset(self):
		ReplacementFormSet = get_replacement_formset()

		if self.request.method == 'POST':
			formset = ReplacementFormSet(self.request.POST, self.request.FILES)
		else:
			formset = ReplacementFormSet()

		return formset

class FixUpdateView(UpdateView):
	model = Fix
	fields = ('problem', 'solution', 'observation', 'equipment')
	success_url = '/fix/'