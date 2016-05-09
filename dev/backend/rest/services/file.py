from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from rest.exceptions.requestException import RequestException, RequestExceptionByCode, RequestExceptionByMessage
from rest.JSONResponse import ResponseJson
from rest.models import File, Level, User, FileType, BannedHash, OkMessage
from rest.models.message.errorMessage import ErrorMessage
from rest.orm.serializers import FileSerializer, FileTypeSerializer, BannedHashSerializer
from rest.orm.unserializer import unserialize_file_binary, unserialize_file
from rest.services.auth import AuthService


class FileService:

    def __init__(self):
        pass

    @staticmethod
    def add(session_token=None, data=None, files=None):
        try:

            uploader_id = User.objects.get(sessionToken=session_token).id
            AuthService.is_authorized_author(session_token=session_token, author_id=uploader_id, level=True)

            Level.validate_exists_level(data['subject_id'])
            Level.validate_subject_type(data['subject_id'])
            fields = ['uploader_id', 'subject_id', 'name', 'text', 'fileType_id']
            new_file = unserialize_file_binary(data, fields=fields, optional=True, binary=files['file'])
            new_file.save()
            return ResponseJson(message_id=OkMessage.Type.FILE_UPLOADED)
        except Exception:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def delete(session_token=None, file_hash=None, **kwargs):
        try:
            model = File.objects.get(hash=file_hash)
            AuthService.is_authorized_author(session_token=session_token, author_id=model.uploader_id, level=True, same=False)
            model.visible = False
            model.save()
            return ResponseJson(message_id=OkMessage.Type.FILE_REMOVED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def metadata_get(file_hash=None, **kwargs):
        try:
            file_returning = File.objects.filter(hash=file_hash, visible=True)
            file_dict = FileSerializer(file_returning, many=True).data
            return ResponseJson(body=file_dict)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def metadata_update(session_token=None, file_hash=None, data=None):
        try:

            file_original = File.objects.get(hash=file_hash)
            AuthService.is_authorized_author(session_token=session_token, author_id=file_original.uploader_id, level=True, same=False)

            fields = ['name', 'text', 'fileType_id']
            file_updated = unserialize_file(data, fields=fields, optional=True)

            file_original.update(file_updated, fields)
            file_original.lastUpdater_id = User.get_signed_user_id(session_token)
            file_original.save()
            return ResponseJson(message_id=OkMessage.Type.FILE_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError or MultiValueDictKeyError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def binary_get(file_hash=None, **kwargs):
        try:
            response_file = File.objects.get(hash=file_hash)

            response = HttpResponse(response_file.file)
            response['Content-Disposition'] = 'attachment; filename=' + response_file.filename
            return response
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def get_banned_hashes():
        hashes = BannedHash.objects.all()
        hash_list = BannedHashSerializer(hashes, many=True).data
        return ResponseJson(body=hash_list)


class FileTypeService:
    def __init__(self):
        pass

    @staticmethod
    def get():
        try:
            return FileTypeService.__get__file_types()
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def __get__file_types():
        files_types = FileType.objects.all()
        file_types_list = FileTypeSerializer(files_types, many=True).data
        return ResponseJson(body=file_types_list)
