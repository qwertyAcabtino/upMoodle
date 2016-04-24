from rest.JSONResponse import JSONResponse
from rest.models import Level, FileType
from rest.orm.serializers import LevelSerializer, FileTypeSerializer


def fileTypes_get():
    filesTypes = FileType.objects.all()
    serializer = FileTypeSerializer(filesTypes, many=True)
    return JSONResponse(serializer.data)
