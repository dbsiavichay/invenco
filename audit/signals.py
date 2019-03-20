# -*- coding: utf-8 -*-
from audit.middleware import RequestMiddleware
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
	

@receiver(post_save)
def audit_log(sender, instance, created, raw, update_fields, **kwargs):
	if not check_allows(sender):
		return

	user = get_user()
	if created:
		instance.save_addition(user)
	elif not raw:
		instance.save_edition(user)

@receiver(post_delete)
def audit_delete_log(sender, instance, **kwargs):
	if not check_allows(sender):
		return

	user = get_user()		
	instance.save_deletion(user)

def check_allows(sender):
	list_of_models = (
		'Brand', 'Type', 'TypeSpecification', 'Set', 'SetDetail', 'Model', 'Assignment', 'Replacement',
		'Fix','Profile','Building','Provider',
	)

	if sender.__name__ in list_of_models:
		return True

	return False

def get_user():
	thread_local = RequestMiddleware.thread_local
	if hasattr(thread_local, 'user'):
		user = thread_local.user
	else:
		user = None

	return user