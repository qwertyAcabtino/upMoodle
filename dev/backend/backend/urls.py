from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin

from backend import settings
from rest.routers import *

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^roles/$', roles_list),

    # APIs
    # System
    url(r'^signup/$', signup),
    url(r'^confirm_email/$', confirm_email),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^recover_password/$', recover_password),

    # User
    url(r'^user/$', user_endpoint),
    url(r'^user/subjects/$', user_subjects),
    url(r'^user/profilePic/$', user_profile_pic),
    url(r'^user/(?P<pk>[0-9]+)/$', user_by_id),
    url(r'^users/rol/(?P<pk>[0-9]+)/$', users_by_rol),

    # Notes
    url(r'^level/(?P<level_id>[0-9]+)/notes(/?)$', notes_by_level_id),
    url(r'^note/(?P<note_id>[0-9]+)/$', note_by_id),
    url(r'^note/$', note_endpoint),

    # Calendar
    url(r'^calendar/(?P<period>(month|day))/(?P<init_date>([0-9]|-)*)/$', calendar_by_period),
    url(r'^calendar/(?P<pk>[0-9]+)/$', calendar_by_id),
    url(r'^calendar/$', calendar_endpoint),

    # Files
    url(r'^file/banned/$', files_banned_hashes),
    url(r'^file/(?P<file_hash>(\w|_)+)(/?)$', file_by_hash_endpoint),
    url(r'^file/$', file_add_endpoint),

    # Subjects
    url(r'^subject/(?P<pk>[0-9]+)/files(/?)$', subject_files_list),
    url(r'^subjectsTree/$', level_tree),
    url(r'^fileTypes/$', filetype_list),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

