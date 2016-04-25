from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.datastructures import MultiValueDictKeyError

from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import is_authorized_author
from rest.models import NoteBoard, Level, User, Message
from rest.models.message.errorMessage import ErrorMessageType
from rest.models.message.message import MessageType
from rest.orm.serializers import NoteBoardSerializer
from rest.orm.unserializer import unserialize_note
from rest.services.level import LevelService


class NoteService:
    def __init__(self):
        pass

    @staticmethod
    def get_note_by_id(note_id=None, **kwargs):
        try:
            note = NoteBoard.objects.get(id=note_id, visible=True)
            serializer = NoteBoardSerializer(note, many=False)
            return JSONResponse(serializer.data)
        except RequestException as r:
            return r.jsonResponse
        except (ObjectDoesNotExist, OverflowError, ValueError):
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def update_note_by_id(session_token=None, note_id=None, data=None, **kwargs):
        try:
            original_note = NoteBoard.objects.get(id=note_id)

            is_authorized_author(session_token=session_token, author_id=original_note.author_id, level=True)

            Level.validate_exists(data)
            fields = ['topic', 'text', 'level_id']
            updated_note = unserialize_note(data, fields=fields, optional=True)
            original_note.update(updated_note, fields)
            original_note.save()
            return JSONResponseID(MessageType.NOTE_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or MultiValueDictKeyError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def delete_note_by_id(session_token=None, note_id=None, data=None, **kwargs):
        try:
            original_note = NoteBoard.objects.get(id=note_id)
            is_authorized_author(session_token=session_token, author_id=original_note.author_id, level=True)

            original_note.visible = False
            original_note.save()
            return JSONResponseID(MessageType.NOTE_REMOVED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def add(session_token=None, data=None):
        try:
            Level.validate_exists(data)
            fields = ['topic', 'text', 'level_id']
            note = unserialize_note(data, fields=fields, optional=True)
            note.author_id = User.get_signed_user_id(session_token)
            note.save()
            message = Message.objects.get(pk=MessageType.NOTE_CREATED.value)
            return JSONResponse({"noteId": note.id, "message": message.message}, status=200)
        except RequestException as r:
            return r.jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def get_notes_by_level_id(level_id=None, data=None):
        try:
            Level.validate_exists_level(level_id)
            if data.get('recursive') and data.get('recursive') == 'true':
                level_group = LevelService.get_level_children_ids_list(level_id=level_id)
            else:
                level_group = (level_id,)
            note = NoteBoard.objects.filter(level_id__in=level_group, visible=True)
            serializer = NoteBoardSerializer(note, many=True)
            return JSONResponse(serializer.data)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
