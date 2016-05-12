from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.datastructures import MultiValueDictKeyError

from upmoodle.models import User
from upmoodle.models.message.errorMessage import ErrorMessage
from upmoodle.models.message.okMessage import OkMessage
from upmoodle.models.utils.jsonResponse import JsonResponse
from upmoodle.models.utils.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from upmoodle.services.orm.unserializer import unserialize_user
from upmoodle.services.utils.randoms import RandomStringsService


class UserService:
    def __init__(self):
        pass

    @staticmethod
    def get_me(session_token=None, **kwargs):
        try:
            user_json = User.query_one(sessionToken=session_token)
            return JsonResponse(body=user_json)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def delete_me(session_token=None, **kwargs):
        deleting_user = User.objects.get(sessionToken=session_token)
        deleting_user.name = 'RemovedUser ' + str(deleting_user.id)
        deleting_user.nick = 'RemovedUser ' + str(deleting_user.id)
        deleting_user.email = 'deprecated+' + deleting_user.email
        deleting_user.password = RandomStringsService.random_password()
        deleting_user.profilePic = 'static/default_update_avatar_pic.jpeg'
        deleting_user.banned = True
        deleting_user.confirmedEmail = False
        deleting_user.save()
        return JsonResponse(message_id=OkMessage.Type.USER_REMOVED)

    @staticmethod
    def update_me(session_token=None, data=None):
        try:
            auth_user = User.objects.get(sessionToken=session_token)
            try:
                assert data['password']
                if not auth_user.password == data['oldPassword']:
                    raise RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA)
            except KeyError:
                pass
            fields = ['nick', 'name', 'password', 'email']
            updated_user = unserialize_user(data, fields=fields, optional=True)
            auth_user.update(updated_user, fields)
            auth_user.save()
            return JsonResponse(message_id=OkMessage.Type.USER_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except KeyError as k:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def update_me_subjects(session_token=None, data=None):
        try:
            if data['ids']:
                subjects = data['ids']
            else:
                subjects = []
            updating_user = User.objects.get(sessionToken=session_token)
            updating_user.update_subjects(subjects)
            updating_user.save()
            return JsonResponse(message_id=OkMessage.Type.USER_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except KeyError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def update_me_avatar(session_token=None, files=None):
        try:
            avatar = files['avatar']
            if "image/" not in avatar.content_type:
                return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
            else:
                auth_user = User.objects.get(sessionToken=session_token)
                auth_user.profilePic = avatar
                auth_user.save()
                return JsonResponse(message_id=OkMessage.Type.USER_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except MultiValueDictKeyError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def get_user_by_id(user_id=None):
        try:
            user_json = User.query_one(id=user_id)
            return JsonResponse(body=user_json)
        except RequestException as r:
            return r.jsonResponse
        except (ObjectDoesNotExist, OverflowError, ValueError):
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse

    @staticmethod
    def get_users_by_rol(rol_id=None):
        try:
            users_json = User.query_many(rol=rol_id, banned=False)
            return JsonResponse(body=users_json)
        except RequestException as r:
            return r.jsonResponse
        except OverflowError:
            return RequestExceptionByCode(ErrorMessage.Type.INCORRECT_DATA).jsonResponse
