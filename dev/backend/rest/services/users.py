import ast

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt

from backend.settings import SESSION_COOKIE_NAME
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import check_signed_in_request, get_random_email, get_random_password
from rest.models import User
from rest.models.message.errorMessage import ErrorMessageType
from rest.models.message.message import MessageType
from rest.orm.serializers import UserSerializer
from rest.orm.unserializer import unserialize_user

# == Signed in user ==


@csrf_exempt
def user_get(request):
    try:
        check_signed_in_request(request, 'GET')
        sessionToken = request.COOKIES[SESSION_COOKIE_NAME]
        users = User.objects.get(sessionToken=sessionToken)
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


@csrf_exempt
def user_delete(request):
    try:
        check_signed_in_request(request, method='DELETE')
        sessionToken = request.COOKIES[SESSION_COOKIE_NAME]
        userSigned = User.objects.get(sessionToken=sessionToken)
        userSigned.name = 'RemovedUser ' + str(userSigned.id)
        userSigned.nick = 'RemovedUser ' + str(userSigned.id)
        userSigned.email = get_random_email()
        userSigned.password = get_random_password()
        userSigned.profilePic = '_default.png'
        userSigned.banned = True
        userSigned.confirmedEmail = False
        userSigned.save()
        return JSONResponseID(MessageType.USER_REMOVED)
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def user_put(request):
    try:
        check_signed_in_request(request, 'POST')
        form = request.POST
        userSigned = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME])
        try:
            password = form['password']
            if not userSigned.password == form['oldPassword']:
                raise RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA)
        except MultiValueDictKeyError:
            pass
        fields = ['nick', 'name', 'password', 'email']
        userUpdated = unserialize_user(form, fields=fields, optional=True)
        userSigned.update(userUpdated, fields)
        userSigned.save()
        return JSONResponseID(MessageType.USER_UPDATED)
    except RequestException as r:
        return r.jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse


def user_put_profile_pic(request):
    try:
        check_signed_in_request(request, 'POST')
        form = request.POST
        profilePic = request.FILES['profilePic']
        if "image/" not in profilePic.content_type:
            return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
        else:
            userSigned = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME])
            userSigned.profilePic = profilePic
            userSigned.save()
            return JSONResponseID(MessageType.USER_UPDATED)
    except RequestException as r:
        return r.jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse


def user_subjects_put(request):
    try:
        check_signed_in_request(request, 'POST')
        form = request.POST
        if form['ids'] and len(form['ids']) > 1:
            subjects = ast.literal_eval(form['ids'])
        elif form['ids'] and len(form['ids']) == 1:
            subjects = [ast.literal_eval(form['ids'])]
        else:
            subjects = []
        userSigned = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME])
        userSigned.update_subjects(subjects)
        userSigned.save()
        return JSONResponseID(MessageType.USER_UPDATED)
    except RequestException as r:
        return r.jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse
    except ValidationError as v:
        return RequestExceptionByMessage(v).jsonResponse

# == Any other user ==
def user_get_id(request, pk):
    try:
        check_signed_in_request(request, 'GET')
        users = User.objects.get(id=pk)
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

# == Rol ==
def user_get_rol(request, rol):
    try:
        check_signed_in_request(request, 'GET')
        users = User.objects.filter(rol=rol, banned=False)
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)
    except RequestException as r:
        return r.jsonResponse
    except OverflowError:
        return RequestExceptionByCode(ErrorMessageType.INCORRECT_DATA).jsonResponse