from upmoodle.models import Rol
from upmoodle.services.utils.zero_exception_decorator import map_exceptions


class RolService:

    def __init__(self):
        pass

    @staticmethod
    @map_exceptions
    def get_roles_list():
        return Rol.objects.all()
