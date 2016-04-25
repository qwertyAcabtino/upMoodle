from rest.JSONResponse import JSONResponse
from rest.models import Rol
from rest.orm.serializers.rol import RolSerializer


class RolService:
    def __init__(self):
        pass

    @staticmethod
    def get_roles_list():
        roles = Rol.objects.all()
        serializer = RolSerializer(roles, many=True)
        return JSONResponse(serializer.data)
