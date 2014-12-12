from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('rest.router',
    # Examples:
    url(r'^bannedhashes/$', 'bannedhashList'),
    # url(r'^users/$', 'usersList'),
    url(r'^roles/$', 'rolesList'),
    url(r'^calendar/$', 'calendarList'),
    url(r'^files/$', 'filesList'),
    url(r'^file/f/(?P<pk>[0-9]+)/$', 'fileBinary'),
    url(r'^file/(?P<pk>[0-9]+)/$', 'file'),
    url(r'^files/subject/(?P<pk>[0-9]+)/$', 'fileListSubject'),
    url(r'^admin/', include(admin.site.urls)),


    # APIs
    # System
    url(r'^signup/$', 'signup'),
    url(r'^confirm_email/(?P<cookie>.*)/$', 'confirmEmail'),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^recover_password/$', 'recoverPassword'),

    # User
    url(r'^user/$', 'user'),
    url(r'^user/(?P<pk>[0-9]+)/$', 'userById'),
    url(r'^users/rol/(?P<pk>[0-9]+)/$', 'usersByRol'),

    # Notes
    url(r'^note/level/(?P<level>[0-9]+)/$', 'noteByLevel'),
    url(r'^note/(?P<pk>[0-9]+)/$', 'noteById'),
    url(r'^note/$', 'note')
)
