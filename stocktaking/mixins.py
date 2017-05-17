from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_unicode

class AuditMixin(object):    
	def save_log(self, obj, ACTION):		
		
		obj = LogEntry.objects.create(
		    user_id         = self.request.user.id, 
		    content_type_id = ContentType.objects.get_for_model(obj).id,
		    object_id       = obj.id,
		    object_repr     = force_unicode(obj), 
		    action_flag     = ACTION
		)

		obj.change_message = str(obj)
		obj.save()

	def save_addition(self, obj):
		self.save_log(obj, ADDITION)

	def save_edition(self, obj):
		self.save_log(obj, CHANGE)

	def save_deletion(self, obj):
		self.save_log(obj, DELETION)