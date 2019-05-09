from django.contrib import admin
from .models import ProblemType, Ticket, Reply

class ProblemTypeAdmin(admin.ModelAdmin):
	pass

class TicketAdmin(admin.ModelAdmin):
	pass

class ReplyAdmin(admin.ModelAdmin):
	pass

admin.site.register(ProblemType, ProblemTypeAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Reply, ReplyAdmin)
