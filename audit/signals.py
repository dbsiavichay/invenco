# -*- coding: utf-8 -*-
from audit.middleware import RequestMiddleware
from django.db.models import signals
from django.dispatch import receiver
	

@receiver(signals.post_save)
def audit_log(sender, instance, created, raw, update_fields, **kwargs):
	if sender.__name__ == 'LogEntry':
		return

	user = get_user()
	if created:
		instance.save_addition(user)
	elif not raw:
		instance.save_edition(user)

@receiver(signals.post_delete)
def audit_delete_log(sender, instance, **kwargs):
	if sender.__name__ == 'LogEntry':
		return

	user = get_user()		
	instance.save_deletion(user)

def get_user():
	thread_local = RequestMiddleware.thread_local
	if hasattr(thread_local, 'user'):
		user = thread_local.user
	else:
		user = None

	return user