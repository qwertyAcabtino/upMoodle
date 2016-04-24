from rest.JSONResponse import JSONResponse
from rest.models import FileType
from rest.orm.serializers import FileTypeSerializer


def fileTypes_get():
    filesTypes = FileType.objects.all()
    serializer = FileTypeSerializer(filesTypes, many=True)
    return JSONResponse(serializer.data)
