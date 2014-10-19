from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('rest.views',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^noteboards/$', 'noteboard_list'),
    url(r'^noteboards/(?P<pk>[0-9]+)/$', 'noteboard_note'),
    url(r'^admin/', include(admin.site.urls)),
)
