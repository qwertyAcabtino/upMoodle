from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.datastructures import MultiValueDictKeyError

from rest.exceptions.requestException import RequestException, RequestExceptionByCode, RequestExceptionByMessage
from rest.JSONResponse import ResponseJson
from rest.models import NoteBoard, Level, User, OkMessage
from rest.models.message.errorMessage import ErrorMessage
from rest.orm.serializers import NoteBoardSerializer
from rest.orm.unserializer import unserialize_note
from rest.services.auth import AuthService
from rest.services.level import LevelService


class NoteService:
    def __init__(self):
        pass

    @staticmethod
    def get_note_by_id(note_id=None, **kwargs):
        try:
            note = NoteBoard.objects.get(id=note_id, visible=True)
            note_dict = NoteBoardSerializer(note, many=False).data
            return ResponseJson(body=note_dict)
        except RequestException as r:
            return r.jsonResponse
        except (ObjectDoesNotExist, OverflowError, ValueError):
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def update_note_by_id(session_token=None, note_id=None, data=None, **kwargs):
        try:
            original_note = NoteBoard.objects.get(id=note_id)

            AuthService.is_authorized_author(session_token=session_token, author_id=original_note.author_id, level=True)

            Level.validate_exists(data)
            fields = ['topic', 'text', 'level_id']
            updated_note = unserialize_note(data, fields=fields, optional=True)
            original_note.update(updated_note, fields)
            original_note.save()
            return ResponseJson(message_id=OkMessage.Type.NOTE_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or MultiValueDictKeyError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def delete_note_by_id(session_token=None, note_id=None, data=None, **kwargs):
        try:
            original_note = NoteBoard.objects.get(id=note_id)
            AuthService.is_authorized_author(session_token=session_token, author_id=original_note.author_id, level=True)

            original_note.visible = False
            original_note.save()
            return ResponseJson(message_id=OkMessage.Type.NOTE_REMOVED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def add(session_token=None, data=None):
        try:
            Level.validate_exists(data)
            fields = ['topic', 'text', 'level_id']
            note = unserialize_note(data, fields=fields, optional=True)
            note.author_id = User.get_signed_user_id(session_token)
            note.save()
            return ResponseJson(body=note, message_id=OkMessage.Type.NOTE_CREATED)
        except RequestException as r:
            return r.jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def get_notes_by_level_id(level_id=None, data=None):
        try:
            Level.validate_exists_level(level_id)
            if data.get('recursive') and data.get('recursive') == 'true':
                level_group = LevelService.get_level_children_ids_list(level_id=level_id)
            else:
                level_group = (level_id,)
            notes = NoteBoard.objects.filter(level_id__in=level_group, visible=True)
            notes_list = NoteBoardSerializer(notes, many=True).data
            return ResponseJson(body=notes_list)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
