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
                       url(r'^confirm_email/$', confirmEmail),
                       url(r'^login/$', login),
                       url(r'^logout/$', logout),
                       url(r'^recover_password/$', recoverPassword),

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
    url(r'^file/(?P<pk>[0-9]+)/binary$', file_binary_operations),  # File's binary download.
    url(r'^file/(?P<pk>[0-9]+)/metadata$', file_metadata_operations),  # File get, post (edit), delete.
    url(r'^file/$', file_binary_upload),  # New file upload. TODo. Remove previous endpoint

    # Subjects
    url(r'^subject/files/(?P<pk>[0-9]+)/$', fileListSubject),

    url(r'^subjectsTree/$', subjectsTree),
    url(r'^fileTypes/$', fileTypes),

    # Deprecated. Todo. remove
    url(r'^file/f/$', file_binary_upload),  # New file upload. TODo. Replace id by file's hash.
    url(r'^file/f/(?P<pk>[0-9]+)/$', file_binary_operations),  # File download. TODO. Remove
    url(r'^files/subject/(?P<pk>[0-9]+)/$', fileListSubject),  # TODO. Remove.

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
