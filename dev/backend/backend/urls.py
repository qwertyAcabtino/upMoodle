from django.conf.urls import include, url, patterns
from django.conf.urls.static import static
from django.contrib import admin

from backend import settings
from rest.routers import *

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    # System
    url(r'^auth/signup/$', signup),
    url(r'^auth/confirm_email/$', confirm_email),
    url(r'^auth/login/$', login),
    url(r'^auth/logout/$', logout),
    url(r'^auth/recover_password/$', recover_password),

    # User
    url(r'^user/$', user_endpoint),
    url(r'^user/subjects/$', user_subjects),
    url(r'^user/avatar/$', user_avatar),
    url(r'^user/(?P<pk>[0-9]+)/$', user_by_id),

    # Rol
    url(r'^rol/_all$', roles_list),
    url(r'^rol/(?P<pk>[0-9]+)/users$', users_by_rol),

    # Notes
    url(r'^note/(?P<note_id>[0-9]+)/$', note_by_id),
    url(r'^note/$', note_endpoint),

    # Calendar
    url(r'^calendar/(?P<period>(month|day))/(?P<init_date>([0-9]|-)*)/$', calendar_by_period),
    url(r'^calendar/(?P<pk>[0-9]+)/$', calendar_by_id),
    url(r'^calendar/$', calendar_endpoint),

    # Files
    # url(r'^file/banned$', files_banned_hashes), Disabled
    url(r'^file/(?P<file_hash>(\w|_)+)(/?)$', file_by_hash_endpoint),
    url(r'^file/$', file_add_endpoint),

    url(r'^filetype/_all$', filetype_list),

    # Level
    url(r'^level/_tree$', level_tree),
    url(r'^level/(?P<level_id>[0-9]+)/notes$', level_notes_list),
    url(r'^level/(?P<level_id>[0-9]+)/files$', level_files_list),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
