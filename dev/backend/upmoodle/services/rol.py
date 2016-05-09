from upmoodle.models import Rol
from upmoodle.models.utils.jsonResponse import JsonResponse
from upmoodle.services.orm.serializers import RolSerializer


class RolService:
    def __init__(self):
        pass

    @staticmethod
    def get_roles_list():
        roles = Rol.objects.all()
        roles_dict = RolSerializer(roles, many=True).data
        return JsonResponse(roles_dict)
