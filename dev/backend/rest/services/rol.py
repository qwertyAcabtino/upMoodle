from rest.JSONResponse import ResponseJson
from rest.models import Rol
from rest.orm.serializers.rol import RolSerializer


class RolService:
    def __init__(self):
        pass

    @staticmethod
    def get_roles_list():
        roles = Rol.objects.all()
        roles_dict = RolSerializer(roles, many=True).data
        return ResponseJson(roles_dict)
