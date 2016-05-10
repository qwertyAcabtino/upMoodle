from upmoodle.routers.decorators.routing_decorators import authenticated, method
from upmoodle.services.file import FileService
from upmoodle.services.level import LevelService
from upmoodle.services.notes import NoteService


@authenticated
@method('GET')
def level_tree(request, **kwargs):
    return LevelService.get_tree()


@authenticated
@method('GET')
def level_notes_list(request, level_id, data=None, **kwargs):
    return NoteService.get_notes_by_level_id(level_id=level_id, data=data)


@authenticated
@method('GET')
def level_files_list(request, level_id, data=None, **kwargs):
    return FileService.get_files_by_level_id(level_id=level_id)
