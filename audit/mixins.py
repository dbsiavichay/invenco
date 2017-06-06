# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_unicode


class AuditMixin(object):    
	def save_log(self, user, message, ACTION):		
		
		log = LogEntry.objects.create(
		    user_id         = user.id, 
		    content_type_id = ContentType.objects.get_for_model(self).id,
		    object_id       = self.id,
		    object_repr     = force_unicode(self), 
		    action_flag     = ACTION,
		    change_message = message
		)


	def save_addition(self, user):
		message = '[{"añadidos": {}}]'
		self.save_log(user, message, ADDITION)

	def save_edition(self, user):
		self.save_log(user, '[{"cambiados": {"fields": []}}]', CHANGE)

	def save_deletion(self, user):
		self.save_log(user, '[{"eliminados": {}}]', DELETION)