from maintenance.models import *
from datetime import timedelta

fixes = Fix.objects.all()

for f in fixes:	
	t = Ticket.objects.create(problem_type_id=1, equipment=f.equipment, problem=f.problem, status=3, user=f.user)
	t.date=f.date_joined
	t.save()
	r = Reply.objects.create(ticket=t, description=f.solution)
	r.date=f.date_joined + timedelta(hours=1)
	r.save()