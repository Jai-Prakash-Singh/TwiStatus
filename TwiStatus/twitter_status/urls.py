from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'status_reply.views.get_status_reply', name='get_status_reply'),
    url(r'^ajax_get_reply/$', 'status_reply.views.ajax_get_reply', name='ajax_get_reply'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
   
)
