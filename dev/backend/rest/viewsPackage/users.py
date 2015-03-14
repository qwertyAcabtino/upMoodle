from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.views.decorators.csrf import csrf_exempt
from backend.settings import SESSION_COOKIE_NAME_BIS
from rest.JSONResponse import JSONResponse, JSONResponseID
from rest.MESSAGES_ID import INCORRECT_DATA, USER_REMOVED, USER_UPDATED
from rest.controllers.Exceptions.requestException import RequestException, RequestExceptionByCode, \
    RequestExceptionByMessage
from rest.controllers.controllers import check_signed_in_request, get_random_email, get_random_password
from rest.models import User
from rest.orm.serializers import UserSerializer
from rest.orm.unserializers import unserialize_user

# == Signed in user ==

@csrf_exempt
def user_get(request):
    try:
        check_signed_in_request(request, 'GET')
        sessionToken = request.COOKIES[SESSION_COOKIE_NAME_BIS]
        users = User.objects.get(sessionToken=sessionToken)
        serializer = UserSerializer(users, many=False)
        return JSONResponse(serializer.data)
    except RequestException as r:
        return r.jsonResponse
    except ObjectDoesNotExist:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except OverflowError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse


@csrf_exempt
def user_delete(request):
    try:
        check_signed_in_request(request, method='DELETE')
        sessionToken = request.COOKIES[SESSION_COOKIE_NAME_BIS]
        userSigned = User.objects.get(sessionToken=sessionToken)
        userSigned.name = 'RemovedUser ' + str(userSigned.id)
        userSigned.nick = 'RemovedUser ' + str(userSigned.id)
        userSigned.email = get_random_email()
        userSigned.password = get_random_password()
        userSigned.profilePic = '_default.png'
        userSigned.banned = True
        userSigned.confirmedEmail = False
        userSigned.save()
        return JSONResponseID(USER_REMOVED)
    except RequestException as r:
        return r.jsonResponse


@csrf_exempt
def user_put(request):
    try:
        check_signed_in_request(request, 'POST')
        form = request.POST
        userSigned = User.objects.get(sessionToken=request.COOKIES[SESSION_COOKIE_NAME_BIS])
        try:
            password = form['password']
            if not userSigned.password == form['oldPassword']:
                raise RequestExceptionByCode(INCORRECT_DATA)
        except MultiValueDictKeyError:
            pass
        fields = ['nick', 'name', 'password', 'email']
        userUpdated = unserialize_user(form, fields=fields, optional=True)
        userSigned.update(userUpdated, fields)
        userSigned.save()
        return JSONResponseID(USER_UPDATED)
    except RequestException as r:
        return r.jsonResponse
    except MultiValueDictKeyError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
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
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except OverflowError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
    except ValueError:
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse

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
        return RequestExceptionByCode(INCORRECT_DATA).jsonResponse
