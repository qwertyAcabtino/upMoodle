import uuid

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from backend import settings
from backend.settings import SESSION_COOKIE_NAME
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.controllers.Exceptions.requestException import RequestExceptionByCode, RequestExceptionByMessage, \
    RequestException
from rest.controllers.controllers import check_cookies, get_email_confirmation_message, cookies_are_ok, \
    get_random_password, send_recover_password_email, check_request_method
from rest.models import User, Level, FileType
from rest.models.message.errorMessage import ErrorMessageType
from rest.models.message.message import MessageType
from rest.orm.serializers import LevelSerializer, FileTypeSerializer
from rest.orm.unserializer import unserialize_user


def confirmEmail_sys(request):
    try:
        check_request_method(request, method='POST')
        token = request.POST['token']
        user = User.objects.get(sessionToken=token)
        if user.confirmedEmail:
            return RequestExceptionByCode(ErrorMessageType.ALREADY_CONFIRMED).jsonResponse
        else:
            user.confirmedEmail = True
            user.save()
            return JSONResponseID(MessageType.ACCOUNT_VALIDATED)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist or OverflowError or ValueError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse


def recoverPassword_sys(request):
    try:
        if request.method == 'POST':
            emailRequest = request.POST['email']
            user = User.objects.get(email=emailRequest)
            if not user.confirmedEmail:
                raise RequestExceptionByCode(ErrorMessageType.UNCONFIRMED_EMAIL)
            elif user.banned:
                raise RequestExceptionByCode(ErrorMessageType.UNAUTHORIZED)
            else:
                password = get_random_password()
                send_recover_password_email(user.email, password)
                user.password = password
                user.save()
        return JSONResponseID(MessageType.RECOVER_PASS_EMAIL)
    except RequestException as r:
        return r.jsonResponse
    except Exception:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse


def subjectsTree_get(id=None):
    if not id:
        subjects = Level.objects.filter(parent=None, visible=True)
        serializer = LevelSerializer(subjects, many=True)
        for item in serializer.data:
            item['children'] = subjectsTree_get(item.get('id'))
        return JSONResponse(serializer.data)
    else:
        subjects = Level.objects.filter(parent=id, visible=True)
        serializer = LevelSerializer(subjects, many=True)
        for item in serializer.data:
            item['children'] = subjectsTree_get(item.get('id'))
            if not item['children'] or len(item['children']) is 0:
                del item['children']
        return serializer.data


def subjectsTree_get_ids(id=None):
    if not id:
        subjects = Level.objects.filter(parent=None, visible=True)
        ids = []
        for subject in subjects:
            ids.append(subject.id)
            ids.extend(subjectsTree_get_ids(subject.id))
        return list(set(ids))
    else:
        subjects = Level.objects.filter(parent=id, visible=True)
        ids = [id]
        for subject in subjects:
            ids.append(subject.id)
            ids.extend(subjectsTree_get_ids(subject.id))
        return list(set(ids))


def fileTypes_get():
    filesTypes = FileType.objects.all()
    serializer = FileTypeSerializer(filesTypes, many=True)
    return JSONResponse(serializer.data)
