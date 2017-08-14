from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
#from stocktaking.urls import stocktaking_router
#from structure.urls import structure_router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('security.urls')),
    url(r'', include('stocktaking.urls')), 
    url(r'', include('structure.urls')),
    url(r'', include('maintenance.urls')),
    url(r'', include('reporting.urls')),
    #url(r'^api/', include(stocktaking_router.urls)),
    #url(r'^api/', include(structure_router.urls)),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
