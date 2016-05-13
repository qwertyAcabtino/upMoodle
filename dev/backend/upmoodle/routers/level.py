from upmoodle.controllers.decorators.exceptions import zero_exceptions
from upmoodle.controllers.decorators.router import authenticated, method
from upmoodle.routers.response.factory import ResponseFactory
from upmoodle.services.file import FileService
from upmoodle.services.level import LevelService
from upmoodle.services.notes import NoteService


@zero_exceptions
@authenticated
@method('GET')
def level_tree(request, **kwargs):
    mapped_levels = LevelService.get_tree()
    return ResponseFactory().ok().body(flatten=mapped_levels).build()


@zero_exceptions
@authenticated
@method('GET')
def level_notes_list(request, level_id, data=None, **kwargs):
    notes = NoteService.get_notes_by_level_id(level_id=level_id, data=data)
    return ResponseFactory().ok().body(obj=notes).build()


@zero_exceptions
@authenticated
@method('GET')
def level_files_list(request, level_id, data=None, **kwargs):
    files = FileService.get_files_by_level_id(level_id=level_id)
    return ResponseFactory().ok().body(obj=files).build()
