from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.datastructures import MultiValueDictKeyError

from upmoodle.models import NoteBoard, Level, User, OkMessage
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.utils.jsonResponse import JsonResponse
from upmoodle.models.utils.requestException import RequestException, RequestExceptionByCode, RequestExceptionByMessage
from upmoodle.services.auth import AuthService
from upmoodle.services.level import LevelService
from upmoodle.services.orm.serializers import NoteBoardSerializer


class NoteService:
    def __init__(self):
        pass

    @staticmethod
    def get_note_by_id(note_id=None, **kwargs):
        try:
            note = NoteBoard.objects.get(id=note_id, visible=True)
            note_dict = NoteBoardSerializer(note, many=False).data
            return JsonResponse(body=note_dict)
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
            updated_note = NoteBoard.parse(data, fields=fields, optional=True)
            original_note.update(updated_note, fields)
            original_note.save()
            return JsonResponse(message_id=OkMessage.Type.NOTE_UPDATED)
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
            return JsonResponse(message_id=OkMessage.Type.NOTE_REMOVED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def add(session_token=None, data=None):
        try:
            Level.validate_exists(data)
            fields = ['topic', 'text', 'level_id']
            note = NoteBoard.parse(data, fields=fields, optional=True)
            note.author_id = User.get_signed_user_id(session_token)
            note.save()
            return JsonResponse(body=note, message_id=OkMessage.Type.NOTE_CREATED)
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
            return JsonResponse(body=notes_list)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
