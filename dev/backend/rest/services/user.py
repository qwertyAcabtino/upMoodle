import ast

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.datastructures import MultiValueDictKeyError

from rest.exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.models import User
from rest.models.message.errorMessage import ErrorMessageType
from rest.models.message.message import MessageType
from rest.orm.serializers import UserSerializer
from rest.orm.unserializer import unserialize_user
from rest.services.utils.email import EmailService
from rest.services.utils.password import PasswordService


class UserService:
    def __init__(self):
        pass

    @staticmethod
    def get_me(session_token=None, **kwargs):
        try:
            users = User.objects.get(sessionToken=session_token)
            serializer = UserSerializer(users, many=False)
            return JSONResponse(serializer.data)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist or OverflowError or ValueError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def delete_me(session_token=None, **kwargs):
        deleting_user = User.objects.get(sessionToken=session_token)
        deleting_user.name = 'RemovedUser ' + str(deleting_user.id)
        deleting_user.nick = 'RemovedUser ' + str(deleting_user.id)
        deleting_user.email = EmailService.get_random_email()
        deleting_user.password = PasswordService.get_random()
        deleting_user.profilePic = '_default.png'
        deleting_user.banned = True
        deleting_user.confirmedEmail = False
        deleting_user.save()
        return JSONResponseID(MessageType.USER_REMOVED)

    @staticmethod
    def update_me(session_token=None, data=None):
        try:
            auth_user = User.objects.get(sessionToken=session_token)
            try:
                assert data['password']
                if not auth_user.password == data['oldPassword']:
                    raise RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA)
            except KeyError:
                pass
            fields = ['nick', 'name', 'password', 'email']
            updated_user = unserialize_user(data, fields=fields, optional=True)
            auth_user.update(updated_user, fields)
            auth_user.save()
            return JSONResponseID(MessageType.USER_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except KeyError as k:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def update_me_subjects(session_token=None, data=None):
        try:
            if data['ids'] and len(data['ids']) > 1:
                subjects = ast.literal_eval(data['ids'])
            elif data['ids'] and len(data['ids']) == 1:
                subjects = [ast.literal_eval(data['ids'])]
            else:
                subjects = []
            updating_user = User.objects.get(sessionToken=session_token)
            updating_user.update_subjects(subjects)
            updating_user.save()
            return JSONResponseID(MessageType.USER_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except KeyError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def update_me_profile_pic(session_token=None, files=None):
        try:
            profile_pic = files['profilePic']
            if "image/" not in profile_pic.content_type:
                return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
            else:
                auth_user = User.objects.get(sessionToken=session_token)
                auth_user.profilePic = profile_pic
                auth_user.save()
                return JSONResponseID(MessageType.USER_UPDATED)
        except RequestException as r:
            return r.jsonResponse
        except MultiValueDictKeyError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except ValidationError as v:
            return RequestExceptionByMessage(v).jsonResponse

    @staticmethod
    def get_user_by_id(user_id=None):
        try:
            users = User.objects.get(id=user_id)
            serializer = UserSerializer(users, many=False)
            return JSONResponse(serializer.data)
        except RequestException as r:
            return r.jsonResponse
        except ObjectDoesNotExist:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except OverflowError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        except ValueError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse

    @staticmethod
    def get_users_by_rol(rol_id=None):
        try:
            users = User.objects.filter(rol=rol_id, banned=False)
            serializer = UserSerializer(users, many=True)
            return JSONResponse(serializer.data)
        except RequestException as r:
            return r.jsonResponse
        except OverflowError:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
