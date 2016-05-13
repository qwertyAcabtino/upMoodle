from upmoodle.models import NoteBoard, Level, User
from upmoodle.routers.decorators.zero_exception_decorator import map_exceptions
from upmoodle.services.auth import AuthService
from upmoodle.services.level import LevelService


class NoteService:
    def __init__(self):
        pass

    @staticmethod
    @map_exceptions
    def get_note_by_id(note_id=None, **kwargs):
        return NoteBoard.objects.get(id=note_id, visible=True)

    @staticmethod
    @map_exceptions
    def update_note_by_id(session_token=None, note_id=None, data=None, **kwargs):
        original_note = NoteBoard.objects.get(id=note_id)

        AuthService.is_authorized_author(session_token=session_token, author_id=original_note.author_id, level=True)

        Level.validate_exists(data)
        fields = ['topic', 'text', 'level_id']
        updated_note = NoteBoard.parse(data, fields=fields, optional=True)
        original_note.update(updated_note, fields)
        original_note.save()

    @staticmethod
    @map_exceptions
    def delete_note_by_id(session_token=None, note_id=None, **kwargs):
        original_note = NoteBoard.objects.get(id=note_id)
        AuthService.is_authorized_author(session_token=session_token, author_id=original_note.author_id, level=True)

        original_note.visible = False
        original_note.save()

    @staticmethod
    @map_exceptions
    def add(session_token=None, data=None):
        Level.validate_exists(data)
        fields = ['topic', 'text', 'level_id']
        note = NoteBoard.parse(data, fields=fields, optional=True)
        note.author_id = User.get_signed_user_id(session_token)
        note.save()
        return note

    @staticmethod
    @map_exceptions
    def get_notes_by_level_id(level_id=None, data=None):
        Level.validate_exists_level(level_id)
        if data.get('recursive') and data.get('recursive') == 'true':
            level_group = LevelService.get_level_children_ids_list(level_id=level_id)
        else:
            level_group = (level_id,)
        return NoteBoard.objects.filter(level_id__in=level_group, visible=True)
