from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('security.urls')),
    url(r'^stocktaking/', include('stocktaking.urls')), 
    url(r'^purchases/', include('purchases.urls')), 
    url(r'', include('structure.urls')),
    url(r'', include('maintenance.urls')),
    url(r'', include('reporting.urls')),    
    url(r'^$', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
