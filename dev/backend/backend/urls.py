from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin

from backend import settings
from rest.router import *

urlpatterns = patterns('',
    url(r'^bannedhashes/$', bannedhashList),
    url(r'^roles/$', rolesList),
    url(r'^admin/', include(admin.site.urls)),

    # APIs
    # System
    url(r'^signup/$', signup),
    url(r'^confirm_email/$', confirm_email),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^recover_password/$', recover_password),

    # User
    url(r'^user/$', user),
    url(r'^user/subjects/$', user_subjects),
    url(r'^user/profilePic/$', user_profilepic),
    url(r'^user/(?P<pk>[0-9]+)/$', userById),
    url(r'^users/rol/(?P<pk>[0-9]+)/$', usersByRol),

    # Notes
    url(r'^note/level/(?P<level>[0-9]+)/$', noteByLevel),
    url(r'^note/(?P<pk>[0-9]+)/$', noteById),
    url(r'^note/$', note),

    # Calendar
    url(r'^calendar/(?P<period>(month|day))/(?P<initDate>([0-9]|-)*)/$', calendarByPeriod),
    url(r'^calendar/(?P<pk>[0-9]+)/$', calendarById),
    url(r'^calendar/$', calendar),

    # Files
    url(r'^file/(?P<file_hash>(\w|_)+)(/?)$', file_by_hash_endpoint),
    url(r'^file/$', file_add_endpoint),

    # Subjects
    url(r'^subject/(?P<pk>[0-9]+)/files(/?)$', fileListSubject),
    url(r'^subjectsTree/$', level_tree),
    url(r'^fileTypes/$', fileTypes),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
