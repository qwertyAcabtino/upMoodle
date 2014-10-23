from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('rest.views',
    # Examples:
    # url(r'^$', 'backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^noteboards/$', 'noteboardList'),
    url(r'^noteboards/(?P<pk>[0-9]+)/$', 'noteboardNote'),
    url(r'^noteboards/level/(?P<pk>[0-9]+)/$', 'noteboardLevel'),
    url(r'^bannedhashes/$', 'bannedhashList'),
    url(r'^users/$', 'usersList'),
    url(r'^users/rol/(?P<pk>[0-9]+)/$', 'usersByRol'),
    url(r'^roles/$', 'rolesList'),
    url(r'^calendar/$', 'calendarList'),
    url(r'^admin/', include(admin.site.urls)),
)
