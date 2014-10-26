from cherrypy.lib.static import serve_file
from django.core.exceptions import ObjectDoesNotExist
from django.utils.importlib import import_module
import mimetypes
from django.utils.encoding import smart_str
import os
from twisted.internet.protocol import FileWrapper
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from backend import settings
from rest.serializers import *


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def noteboardList(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        notes = NoteBoard.objects.all()
        serializer = NoteBoardSerializer(notes, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NoteBoardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def noteboardNote(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        note = NoteBoard.objects.get(pk=pk)
    except NoteBoard.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NoteBoardSerializer(note)
        return JSONResponse(serializer.data)


@csrf_exempt
def noteboardLevel(request, pk):
    """
    Retrieves the noteboards from a level.
    """
    if request.method == 'GET':
        notes = NoteBoard.objects.filter(level=pk)
        serializer = NoteBoardSerializer(notes, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def bannedhashList(request):
    """
    Retrieves the banned file's hash list.
    """
    if request.method == 'GET':
        hashes = BannedHash.objects.all()
        serializer = BannedHashSerializer(hashes, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def usersList(request):
    """
    Retrieves an user's list.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def usersByRol(request, pk):
    """
    Retrieves an user's list filtered by rol.
    """
    if request.method == 'GET':
        users = User.objects.filter(rol=pk)
        serializer = UserSerializer(users, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def rolesList(request):
    """
    Retrieves an user's list filtered by rol.
    """
    if request.method == 'GET':
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def calendarList(request):
    """
    Retrieves user's future calendar events.
    """
    # Todo. Restrict to logged user.
    if request.method == 'GET':
        events = CalendarRegularEvent.objects.all()
        serializer = CalendarEventSerializer(events, many=True)
        return JSONResponse(serializer.data)


def filesList(request):
    """
    Retrieves a file's list .
    """
    if request.method == 'GET':
        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)


def file(request, pk):
    """
    Retrieves a file information.
    """
    if request.method == 'GET':
        files = File.objects.filter(id=pk)
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)


def fileBinary(request, pk):
    file = File.objects.get(id=pk)
    path_to_file = file.file.path

    extension = file.extension()
    f = open(path_to_file, 'r')
    myfile = File(f)
    response = HttpResponse(file.file)
    response['Content-Disposition'] = 'attachment; filename=' + file.name + '.' + extension
    return response


def fileListSubject(request, pk):
    level = Level.objects.get(id=pk)
    if level.is_subject() and request.method == 'GET':
        files = File.objects.filter(subject=pk)
        serializer = FileSerializer(files, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def login(request):
    # engine = import_module(settings.SESSION_ENGINE)
    # session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)

    if request.method == 'POST':
        try:
            session_key = request.session.session_key
            emailIn = request.POST['email']
            passwordIn = request.POST['password']
            try:
                user = User.objects.get(email=emailIn, password=passwordIn)
            except ObjectDoesNotExist:
                raise Exception('Incorrect sign in values')
            user.sessionToken = session_key
            user.save()
            message = Message()
            message.message = 'Successfully signed in.'
            serializer = MessageSerializer(message, many=False)
            jsonResponse = JSONResponse(serializer.data, status=201)

            jsonResponse.set_cookie(settings.SESSION_COOKIE_NAME, session_key)
            return jsonResponse
        except Exception as e:
            error = ErrorMessage(e.message)
            error.error = e.message
            serializer = ErrorMessageSerializer(error, many=False)
            return JSONResponse(serializer.data, status=400)
