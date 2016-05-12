from upmoodle.models import Rol
from upmoodle.models.utils.jsonResponse import JsonResponse


class RolService:

    def __init__(self):
        pass

    @staticmethod
    def get_roles_list():
        roles_dict = Rol.query_many()
        return JsonResponse(body=roles_dict)
