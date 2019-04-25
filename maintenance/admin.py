from django.contrib import admin
from .models import ProblemType

class ProblemTypeAdmin(admin.ModelAdmin):
	pass


admin.site.register(ProblemType, ProblemTypeAdmin)
