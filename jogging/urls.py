from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from core.views import EntryResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(EntryResource())
v1_api.register(UserResource())


urlpatterns = patterns('',
    url(r'', include('core.urls', namespace='core')),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
