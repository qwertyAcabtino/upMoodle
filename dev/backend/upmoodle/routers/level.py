from upmoodle.routers.decorators.routing_decorators import authenticated, method
from upmoodle.routers.decorators.zero_exception_decorator import zero_exceptions
from upmoodle.routers.response.jsonfactory import JsonResponseFactory
from upmoodle.services.file import FileService
from upmoodle.services.level import LevelService
from upmoodle.services.notes import NoteService


@authenticated
@method('GET')
def level_tree(request, **kwargs):
    return LevelService.get_tree()


@authenticated
@method('GET')
@zero_exceptions
def level_notes_list(request, level_id, data=None, **kwargs):
    notes = NoteService.get_notes_by_level_id(level_id=level_id, data=data)
    return JsonResponseFactory().ok().body(obj=notes).build()


@authenticated
@method('GET')
@zero_exceptions
def level_files_list(request, level_id, data=None, **kwargs):
    files = FileService.get_files_by_level_id(level_id=level_id)
    return JsonResponseFactory().ok().body(obj=files).build()
